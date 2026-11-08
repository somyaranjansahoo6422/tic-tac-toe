import tkinter as tk
from tkinter import messagebox
import importlib

try:
    pygame = importlib.import_module("pygame")
except Exception:
    pygame = None

# =========================
# SOUND INITIALIZATION
# =========================
click_sound = None
win_sound = None
if pygame is not None:
    try:
        pygame.mixer.init()
        try:
            click_sound = pygame.mixer.Sound("assets/click.wav")
        except Exception:
            click_sound = None
        try:
            win_sound = pygame.mixer.Sound("assets/win.wav")
        except Exception:
            win_sound = None
    except Exception:
        click_sound = None
        win_sound = None


# =========================
# MAIN GAME CLASS
# =========================
class TicTacToe:

    def __init__(self, root):

        self.root = root

        # Window Settings
        self.root.title("Advanced Tic Tac Toe")

        # Responsive window size
        self.root.geometry("700x850")
        self.root.minsize(700, 850)

        # Allow resizing
        self.root.resizable(True, True)

        # Background color
        self.root.configure(bg="#1e1e2f")

        # Optional fullscreen/maximize
        # self.root.state('zoomed')

        # Game Variables
        self.current_player = "X"
        self.board = ["" for _ in range(9)]
        self.game_over = False

        # Scoreboard
        self.player_score = 0
        self.ai_score = 0
        self.draw_score = 0

        # Game Mode
        self.mode = tk.StringVar(value="AI")
        self.mode.trace_add("write", self.on_mode_change)

        self.winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        # Create UI
        self.create_ui()

    # =========================
    # UI DESIGN
    # =========================
    def create_ui(self):

        # Title
        title = tk.Label(
            self.root,
            text="TIC TAC TOE",
            font=("Arial", 32, "bold"),
            bg="#1e1e2f",
            fg="white"
        )
        title.pack(pady=20)

        # -------------------------
        # MODE SELECTION
        # -------------------------
        mode_frame = tk.Frame(self.root, bg="#1e1e2f")
        mode_frame.pack(pady=10, fill="x", padx=20)

        tk.Radiobutton(
            mode_frame,
            text="Vs AI",
            variable=self.mode,
            value="AI",
            font=("Arial", 14),
            bg="#1e1e2f",
            fg="white",
            selectcolor="#333333",
            activebackground="#1e1e2f",
            activeforeground="white"
        ).pack(side=tk.LEFT, padx=20)

        tk.Radiobutton(
            mode_frame,
            text="2 Players",
            variable=self.mode,
            value="2P",
            font=("Arial", 14),
            bg="#1e1e2f",
            fg="white",
            selectcolor="#333333",
            activebackground="#1e1e2f",
            activeforeground="white"
        ).pack(side=tk.LEFT, padx=20)

        # -------------------------
        # STATUS LABEL
        # -------------------------
        self.status_label = tk.Label(
            self.root,
            text="Player X Turn",
            font=("Arial", 18, "bold"),
            bg="#1e1e2f",
            fg="#00ffcc"
        )
        self.status_label.pack(pady=15, fill="x", padx=20)

        # -------------------------
        # SCOREBOARD
        # -------------------------
        self.score_label = tk.Label(
            self.root,
            text="Player X: 0   AI/O: 0   Draws: 0",
            font=("Arial", 16),
            bg="#1e1e2f",
            fg="white"
        )
        self.score_label.pack(pady=10, fill="x", padx=20)

        # -------------------------
        # GAME BOARD FRAME
        # -------------------------
        self.frame = tk.Frame(self.root, bg="#1e1e2f")
        self.frame.pack(expand=True, fill="both", pady=20)

        # Make grid responsive
        for i in range(3):
            self.frame.grid_rowconfigure(i, weight=1)
            self.frame.grid_columnconfigure(i, weight=1)

        self.buttons = []

        # -------------------------
        # CREATE GAME BUTTONS
        # -------------------------
        for i in range(9):

            btn = tk.Button(
                self.frame,
                text="",
                font=("Arial", 36, "bold"),
                bg="#2d2d44",
                fg="white",
                relief=tk.FLAT,
                activebackground="#444466",
                activeforeground="white",
                bd=0,
                command=lambda i=i: self.make_move(i)
            )

            btn.grid(
                row=i // 3,
                column=i % 3,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            self.buttons.append(btn)

        # -------------------------
        # CONTROL BUTTONS
        # -------------------------
        control_frame = tk.Frame(self.root, bg="#1e1e2f")
        control_frame.pack(pady=20, fill="x", padx=20)

        restart_btn = tk.Button(
            control_frame,
            text="Restart Game",
            font=("Arial", 14, "bold"),
            bg="#00b894",
            fg="white",
            padx=25,
            pady=10,
            relief=tk.FLAT,
            command=self.restart_game
        )

        restart_btn.grid(row=0, column=0, padx=10, sticky="ew")

        reset_btn = tk.Button(
            control_frame,
            text="Reset Scores",
            font=("Arial", 14, "bold"),
            bg="#0984e3",
            fg="white",
            padx=25,
            pady=10,
            relief=tk.FLAT,
            command=self.reset_scores
        )

        reset_btn.grid(row=0, column=1, padx=10, sticky="ew")

        exit_btn = tk.Button(
            control_frame,
            text="Exit",
            font=("Arial", 14, "bold"),
            bg="#d63031",
            fg="white",
            padx=35,
            pady=10,
            relief=tk.FLAT,
            command=self.root.quit
        )

        exit_btn.grid(row=0, column=2, padx=10, sticky="ew")

        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)
        control_frame.grid_columnconfigure(2, weight=1)

    # =========================
    # PLAY SOUND
    # =========================
    def play_sound(self, sound):
        if sound:
            sound.play()

    # =========================
    # MODE CHANGE AND RESET
    # =========================
    def on_mode_change(self, *args):
        self.restart_game()
        self.update_scoreboard()

    def reset_scores(self):
        self.player_score = 0
        self.ai_score = 0
        self.draw_score = 0
        self.update_scoreboard()

    # =========================
    # MAKE MOVE
    # =========================
    def make_move(self, index):

        if self.board[index] == "" and not self.game_over:

            self.board[index] = self.current_player

            self.buttons[index].config(
                text=self.current_player
            )

            self.play_sound(click_sound)

            # Check Winner
            if self.check_winner(self.current_player):

                self.end_game(
                    f"Player {self.current_player} Wins!"
                )

                if self.current_player == "X":
                    self.player_score += 1
                else:
                    self.ai_score += 1

                self.update_scoreboard()
                return

            # Draw
            elif "" not in self.board:

                self.draw_score += 1
                self.update_scoreboard()

                self.end_game("It's a Draw!")
                return

            # Switch Turn
            self.switch_player()

            # AI Move
            if (
                self.mode.get() == "AI"
                and self.current_player == "O"
            ):
                self.root.after(500, self.ai_move)

    # =========================
    # SWITCH PLAYER
    # =========================
    def switch_player(self):

        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

        self.status_label.config(
            text=f"Player {self.current_player} Turn"
        )

    # =========================
    # AI MOVE USING MINIMAX
    # =========================
    def ai_move(self):

        best_score = -float("inf")
        best_move = None

        for i in range(9):

            if self.board[i] == "":

                self.board[i] = "O"

                score = self.minimax(
                    self.board,
                    0,
                    False
                )

                self.board[i] = ""

                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.make_move(best_move)

    # =========================
    # MINIMAX ALGORITHM
    # =========================
    def minimax(self, board, depth, is_maximizing):

        if self.check_winner_on_board(board, "O"):
            return 1

        elif self.check_winner_on_board(board, "X"):
            return -1

        elif "" not in board:
            return 0

        if is_maximizing:

            best_score = -float("inf")

            for i in range(9):

                if board[i] == "":

                    board[i] = "O"

                    score = self.minimax(
                        board,
                        depth + 1,
                        False
                    )

                    board[i] = ""

                    best_score = max(
                        score,
                        best_score
                    )

            return best_score

        else:

            best_score = float("inf")

            for i in range(9):

                if board[i] == "":

                    board[i] = "X"

                    score = self.minimax(
                        board,
                        depth + 1,
                        True
                    )

                    board[i] = ""

                    best_score = min(
                        score,
                        best_score
                    )

            return best_score

    def check_winner_on_board(self, board, player):

        for combo in self.winning_combinations:

            if all(
                board[i] == player
                for i in combo
            ):
                return combo

        return None

    # =========================
    # CHECK WINNER
    # =========================
    def check_winner(self, player):

        combo = self.check_winner_on_board(self.board, player)

        if combo:
            for i in combo:
                self.buttons[i].config(
                    bg="#00cec9"
                )
            return True

        return False

    # =========================
    # END GAME
    # =========================
    def end_game(self, message):

        self.game_over = True

        self.status_label.config(
            text=message
        )

        self.play_sound(win_sound)

        messagebox.showinfo(
            "Game Over",
            message
        )

    # =========================
    # RESTART GAME
    # =========================
    def restart_game(self):

        self.board = ["" for _ in range(9)]

        self.game_over = False

        self.current_player = "X"

        for btn in self.buttons:

            btn.config(
                text="",
                bg="#2d2d44"
            )

        self.status_label.config(
            text="Player X Turn"
        )

    # =========================
    # UPDATE SCOREBOARD
    # =========================
    def update_scoreboard(self):

        ai_text = (
            "AI"
            if self.mode.get() == "AI"
            else "Player O"
        )

        self.score_label.config(
            text=
            f"Player X: {self.player_score}   "
            f"{ai_text}: {self.ai_score}   "
            f"Draws: {self.draw_score}"
        )


# =========================
# MAIN PROGRAM
# =========================
if __name__ == "__main__":

    root = tk.Tk()

    game = TicTacToe(root)

    root.mainloop()
