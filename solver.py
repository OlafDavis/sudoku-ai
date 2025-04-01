import numpy as np
import time

class SudokuSolver:
    def __init__(self, board, groups=None, solve_delay=0.05):
        self.board = board
        self.groups = groups or []  # List of tuples: ([(row1, col1), (row2, col2)], target_sum)
        self.solve_delay = solve_delay
        self.last_solve_time = 0
        self.solving = False
        self.current_cell = None  # Track current cell being examined
        self.last_change = None  # Track the last cell we changed
        self.no_changes_in_pass = True  # Track if we've made any changes in this pass

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
        
        # Check group constraints
        for group, target_sum in self.groups:
            if pos in group:
                # Calculate current sum of filled cells in the group
                current_sum = sum(self.board[r, c] for r, c in group if self.board[r, c] != 0)
                # Add the new number
                new_sum = current_sum + num
                
                # If this is the last empty cell in the group
                empty_cells = sum(1 for r, c in group if self.board[r, c] == 0)
                if empty_cells == 1:
                    if new_sum != target_sum:
                        return False
                # If there are still empty cells
                else:
                    # Check if the new sum would exceed the target
                    if new_sum >= target_sum:
                        return False
                    # Check if remaining cells could make up the difference
                    min_possible = empty_cells - 1  # Minimum possible sum for remaining cells
                    if new_sum + min_possible > target_sum:
                        return False
        
        return True

    def get_possible_numbers(self, pos):
        """Get all possible numbers that could go in a cell."""
        row, col = pos
        if self.board[row, col] != 0:
            return set()
        
        # Start with all numbers 1-9
        possible = set(range(1, 10))
        
        # Remove numbers that appear in the row
        possible -= set(self.board[row])
        
        # Remove numbers that appear in the column
        possible -= set(self.board[:, col])
        
        # Remove numbers that appear in the 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        box_numbers = set(self.board[box_row:box_row+3, box_col:box_col+3].flatten())
        possible -= box_numbers
        
        # Apply group constraints
        for group, target_sum in self.groups:
            if pos in group:
                # Calculate current sum of filled cells
                current_sum = sum(self.board[r, c] for r, c in group if self.board[r, c] != 0)
                # Count empty cells
                empty_cells = sum(1 for r, c in group if self.board[r, c] == 0)
                
                if empty_cells == 1:
                    # If this is the last empty cell, only allow the number that makes sum = target
                    required = target_sum - current_sum
                    if required in possible:
                        possible = {required}
                    else:
                        possible = set()
                else:
                    # If there are still empty cells, remove numbers that would make sum > target
                    max_allowed = target_sum - current_sum - (empty_cells - 1)
                    possible = {n for n in possible if n <= max_allowed}
        
        return possible

    def solve_step_by_step(self):
        if not self.solving:
            return False

        current_time = time.time()
        if current_time - self.last_solve_time < self.solve_delay:
            return False

        # Move to next cell if we made a change
        if self.last_change is not None:
            row, col = self.last_change
            if col < 8:
                self.current_cell = (row, col + 1)
            elif row < 8:
                self.current_cell = (row + 1, 0)
            else:
                self.current_cell = (0, 0)
            self.last_change = None
            self.last_solve_time = current_time
            return True

        # If we don't have a current cell, start from beginning
        if self.current_cell is None:
            self.current_cell = (0, 0)
            self.no_changes_in_pass = True
            self.last_solve_time = current_time
            return True

        # Get possible numbers for current cell
        if self.board[self.current_cell[0], self.current_cell[1]] == 0:
            possible = self.get_possible_numbers(self.current_cell)
            
            # Check if this is the only possible number
            if len(possible) == 1:
                # We found a cell with only one possible number
                num = possible.pop()
                self.board[self.current_cell[0], self.current_cell[1]] = num
                self.last_change = self.current_cell
                self.no_changes_in_pass = False
                self.last_solve_time = current_time
                return True

        # Move to next cell
        row, col = self.current_cell
        if col < 8:
            self.current_cell = (row, col + 1)
        elif row < 8:
            self.current_cell = (row + 1, 0)
        else:
            # We've reached the end of the grid
            if self.no_changes_in_pass:
                # If we made no changes in this pass, we're done
                self.solving = False
                return True
            # Otherwise, start a new pass
            self.current_cell = (0, 0)
            self.no_changes_in_pass = True

        self.last_solve_time = current_time
        return True

    def start_solving(self):
        self.solving = True
        self.last_solve_time = 0
        self.current_cell = (0, 0)
        self.last_change = None
        self.no_changes_in_pass = True

    def stop_solving(self):
        self.solving = False
        self.current_cell = None
        self.last_change = None
        self.no_changes_in_pass = True 