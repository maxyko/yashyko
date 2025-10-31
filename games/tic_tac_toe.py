import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)
        
        # Game state
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(
            self.root, 
            text="Tic Tac Toe", 
            font=("Arial", 24, "bold"),
            pady=10
        )
        self.title_label.pack()
        
        # Current player label
        self.status_label = tk.Label(
            self.root,
            text=f"Current Player: {self.current_player}",
            font=("Arial", 14),
            pady=10
        )
        self.status_label.pack()
        
        # Game board frame
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=20)
        
        # Create buttons for the board
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Arial", 40, "bold"),
                    width=3,
                    height=1,
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                button.grid(row=i, column=j, padx=2, pady=2)
                row.append(button)
            self.buttons.append(row)
        
        # Reset button
        self.reset_button = tk.Button(
            self.root,
            text="Reset Game",
            font=("Arial", 14),
            command=self.reset_game,
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            padx=20,
            pady=10
        )
        self.reset_button.pack(pady=10)
        
    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != "":
            return
        
        # Update board
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(
            text=self.current_player,
            state=tk.DISABLED,
            disabledforeground="blue" if self.current_player == "X" else "red"
        )
        
        # Check for winner or tie
        if self.check_winner():
            self.status_label.config(text=f"Player {self.current_player} Wins!")
            self.game_over = True
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
        elif self.check_tie():
            self.status_label.config(text="It's a Tie!")
            self.game_over = True
            messagebox.showinfo("Game Over", "It's a tie!")
        else:
            # Switch player
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=f"Current Player: {self.current_player}")
    
    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != "":
                return True
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return True
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        
        return False
    
    def check_tie(self):
        for row in self.board:
            if "" in row:
                return False
        return True
    
    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        
        # Reset buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state=tk.NORMAL)
        
        # Reset status label
        self.status_label.config(text=f"Current Player: {self.current_player}")


def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()


if __name__ == "__main__":
    main()

