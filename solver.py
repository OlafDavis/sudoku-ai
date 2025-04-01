import numpy as np
import time

class SudokuSolver:
    def __init__(self, board, solve_delay=0.05):
        self.board = board
        self.solve_delay = solve_delay
        self.last_solve_time = 0
        self.filled_cells = []
        self.tried_numbers = {}
        self.solving = False

    def is_valid_move(self, num, pos):
        row, col = pos
        # Check row
        if num in self.board[row]:
            return False
        # Check column
        if num in self.board[:, col]:
            return False
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        if num in self.board[box_row:box_row+3, box_col:box_col+3]:
            return False
        return True

    def solve_step_by_step(self):
        if self.solving:
            current_time = time.time()
            if current_time - self.last_solve_time < self.solve_delay:
                return False
            
            # Find next empty cell
            for i in range(9):
                for j in range(9):
                    if self.board[i, j] == 0:
                        # Initialize tried numbers for this cell if not exists
                        if (i, j) not in self.tried_numbers:
                            self.tried_numbers[(i, j)] = set()
                        
                        # Try numbers 1-9 that haven't been tried yet
                        for num in range(1, 10):
                            if num not in self.tried_numbers[(i, j)] and self.is_valid_move(num, (i, j)):
                                self.board[i, j] = num
                                self.filled_cells.append((i, j))  # Track this cell
                                self.last_solve_time = current_time
                                return True
                        
                        # If no valid number found, backtrack
                        if self.filled_cells:  # If we have cells to backtrack
                            last_i, last_j = self.filled_cells.pop()  # Get the last filled cell
                            self.board[last_i, last_j] = 0  # Clear it
                            # Add the number we just tried to the tried_numbers set
                            self.tried_numbers[(last_i, last_j)].add(self.board[last_i, last_j])
                            return True
                        else:  # If we can't backtrack anymore, puzzle is unsolvable
                            self.solving = False
                            return False
            
            # If no empty cells found, puzzle is solved
            self.solving = False
            return True
        return False

    def start_solving(self):
        self.solving = True
        self.last_solve_time = 0
        self.filled_cells = []  # Reset the filled cells list
        self.tried_numbers = {}  # Reset the tried numbers dictionary

    def stop_solving(self):
        self.solving = False
        self.filled_cells = []  # Clear the filled cells list
        self.tried_numbers = {}  # Clear the tried numbers dictionary 