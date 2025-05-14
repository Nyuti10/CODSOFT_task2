import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe - AI vs Human")
        self.window.configure(bg='#2C3E50')
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        self.difficulty = "Medium"
        self.human_score = 0
        self.ai_score = 0

        self.create_board()

        self.score_frame = tk.Frame(self.window, bg='#2C3E50')
        self.score_frame.grid(row=0, column=0, columnspan=3, pady=10)

        self.human_score_label = tk.Label(
            self.score_frame, text="Human: 0",
            font=('Helvetica', 12), bg='#2C3E50', fg='#3498DB'
        )
        self.human_score_label.pack(side=tk.LEFT, padx=20)

        self.ai_score_label = tk.Label(
            self.score_frame, text="AI: 0",
            font=('Helvetica', 12), bg='#2C3E50', fg='#E74C3C'
        )
        self.ai_score_label.pack(side=tk.LEFT, padx=20)

        self.difficulty_frame = tk.Frame(self.window, bg='#2C3E50')
        self.difficulty_frame.grid(row=1, column=0, columnspan=3, pady=5)

        self.difficulty_label = tk.Label(
            self.difficulty_frame, text="Difficulty:",
            font=('Helvetica', 12), bg='#2C3E50', fg='white'
        )
        self.difficulty_label.pack(side=tk.LEFT, padx=5)

        self.difficulty_var = tk.StringVar(value="Medium")
        for diff in ["Easy", "Medium", "Hard"]:
            rb = tk.Radiobutton(
                self.difficulty_frame, text=diff,
                variable=self.difficulty_var, value=diff,
                command=self.change_difficulty,
                bg='#2C3E50', fg='white',
                selectcolor='#34495E', activebackground='#2C3E50',
                activeforeground='white'
            )
            rb.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(
            self.window, text="Your turn (X)",
            font=('Helvetica', 14), bg='#2C3E50', fg='white'
        )
        self.status_label.grid(row=5, column=0, columnspan=3, pady=10)

        self.reset_button = tk.Button(
            self.window, text="New Game",
            font=('Helvetica', 12), command=self.reset_game,
            bg='#E74C3C', fg='white', activebackground='#C0392B'
        )
        self.reset_button.grid(row=6, column=0, columnspan=3, pady=10)

    def change_difficulty(self):
        self.difficulty = self.difficulty_var.get()
        self.reset_game()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.window, text="", font=('Helvetica', 20, 'bold'),
                    width=5, height=2,
                    command=lambda row=i, col=j: self.make_move(row, col),
                    bg='#34495E', fg='white',
                    activebackground='#2C3E50'
                )
                button.grid(row=i+2, column=j, padx=5, pady=5)
                self.buttons.append(button)

    def make_move(self, row, col):
        index = row * 3 + col
        if self.board[index] == "":
            self.board[index] = "X"
            self.buttons[index].config(text="X", fg='#3498DB')

            winner = self.check_winner()
            if winner == "X":
                self.human_score += 1
                self.update_score()
                self.status_label.config(text="You win!")
                self.disable_all_buttons()
                return
            elif winner == "O":
                self.ai_score += 1
                self.update_score()
                self.status_label.config(text="AI wins!")
                self.disable_all_buttons()
                return
            elif "" not in self.board:
                self.status_label.config(text="It's a draw!")
                return

            self.status_label.config(text="AI is thinking...")
            self.window.update()

            ai_move = self.get_ai_move()
            self.board[ai_move] = "O"
            self.buttons[ai_move].config(text="O", fg='#E74C3C')

            winner = self.check_winner()
            if winner == "X":
                self.human_score += 1
                self.update_score()
                self.status_label.config(text="You win!")
                self.disable_all_buttons()
                return
            elif winner == "O":
                self.ai_score += 1
                self.update_score()
                self.status_label.config(text="AI wins!")
                self.disable_all_buttons()
                return
            elif "" not in self.board:
                self.status_label.config(text="It's a draw!")
                return

            self.status_label.config(text="Your turn (X)")

    def get_ai_move(self):
        if self.difficulty == "Easy":
            return self.get_random_move()
        elif self.difficulty == "Medium":
            return self.get_medium_move()
        else:
            return self.get_best_move()

    def get_random_move(self):
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        return random.choice(empty_cells)

    def get_medium_move(self):
        if random.random() < 0.5:
            return self.get_random_move()
        return self.get_best_move()

    def get_best_move(self):
        best_score = float('-inf')
        best_move = 0
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(0, False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, depth, is_maximizing):
        winner = self.check_winner()
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif "" not in self.board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "O"
                    score = self.minimax(depth + 1, False)
                    self.board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "X"
                    score = self.minimax(depth + 1, True)
                    self.board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in win_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] ==
                self.board[combo[2]] != ""):
                return self.board[combo[0]]
        return None

    def disable_all_buttons(self):
        for button in self.buttons:
            button.config(state='disabled')

    def update_score(self):
        self.human_score_label.config(text=f"Human: {self.human_score}")
        self.ai_score_label.config(text=f"AI: {self.ai_score}")

    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        for button in self.buttons:
            button.config(text="", state='normal')
        self.status_label.config(text="Your turn (X)")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
