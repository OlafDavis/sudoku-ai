import numpy as np
import pygame
import random
from puzzle_generator import PuzzleGenerator
from solver import SudokuSolver

class Sudoku:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        self.solution = np.zeros((9, 9), dtype=int)
        self.selected = None
        self.original_numbers = set()
        self.solved = False
        self.solver = None
        self.groups = []  # List of tuples: ([(row1, col1), (row2, col2)], target_sum)
        self.generate_puzzle()
        self.generate_groups()

    def generate_puzzle(self):
        self.board, self.solution, self.original_numbers = PuzzleGenerator.generate_puzzle()
        self.generate_groups()  # Generate groups after we have the solution
        self.solver = SudokuSolver(self.board, self.groups)
        self.solved = False

    def generate_groups(self):
        # Create groups of exactly 3 cells that sum to a target number
        possible_groups = []
        
        # Generate all possible 3-cell L shapes
        for i in range(8):
            for j in range(8):
                # L shape pointing right and down
                l_shape1 = [(i, j), (i, j+1), (i+1, j)]
                possible_groups.append(l_shape1)
                # L shape pointing right and up
                l_shape2 = [(i, j), (i, j+1), (i-1, j)]
                if i > 0:
                    possible_groups.append(l_shape2)
                # L shape pointing left and down
                l_shape3 = [(i, j), (i, j-1), (i+1, j)]
                if j > 0:
                    possible_groups.append(l_shape3)
                # L shape pointing left and up
                l_shape4 = [(i, j), (i, j-1), (i-1, j)]
                if i > 0 and j > 0:
                    possible_groups.append(l_shape4)
        
        # Generate all possible 3-cell lines
        for i in range(9):
            for j in range(7):
                # Horizontal line
                h_line = [(i, j), (i, j+1), (i, j+2)]
                possible_groups.append(h_line)
                # Vertical line
                v_line = [(j, i), (j+1, i), (j+2, i)]
                possible_groups.append(v_line)
        
        # Randomly select groups until we find 4 that sum to a target number and don't overlap or touch
        selected_groups = []
        random.shuffle(possible_groups)
        
        def cells_adjacent(cell1, cell2):
            """Check if two cells are adjacent (including diagonally)."""
            r1, c1 = cell1
            r2, c2 = cell2
            return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1
        
        def groups_overlap_or_touch(group1, group2):
            """Check if two groups share any cells or have adjacent cells."""
            # Check for overlapping cells
            if any(cell in group2 for cell in group1):
                return True
            
            # Check for adjacent cells
            for cell1 in group1:
                for cell2 in group2:
                    if cells_adjacent(cell1, cell2):
                        return True
            
            return False
        
        for group in possible_groups:
            if len(selected_groups) >= 4:
                break
            
            # Calculate the sum of numbers in this group
            group_sum = sum(self.solution[r, c] for r, c in group)
            
            # Only select groups where the sum is between 15 and 20
            # (reasonable range for 3 numbers from 1-9)
            if 15 <= group_sum <= 20:
                # Check if this group overlaps or touches any already selected groups
                overlaps = False
                for selected_group, _ in selected_groups:
                    if groups_overlap_or_touch(group, selected_group):
                        overlaps = True
                        break
                
                if not overlaps:
                    selected_groups.append((group, group_sum))
        
        # Store the groups and their target sums
        self.groups = selected_groups

    def handle_click(self, pos, cell_size):
        x, y = pos
        if 0 <= x < 9 * cell_size and 0 <= y < 9 * cell_size:
            row = y // cell_size
            col = x // cell_size
            if (row, col) not in self.original_numbers:
                self.selected = (row, col)
                return True
        return False

    def handle_key(self, key):
        if self.selected is None:
            return
        
        row, col = self.selected
        if key in range(pygame.K_1, pygame.K_9 + 1):
            num = key - pygame.K_1 + 1
            if self.solver.is_valid_move(num, (row, col)):
                self.board[row, col] = num
            return True
        elif key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
            self.board[row, col] = 0
            return True
        return False

    def reveal_solution(self):
        self.board = self.solution.copy()
        self.solved = True

    def reset_puzzle(self):
        self.board = np.zeros((9, 9), dtype=int)
        for i, j in self.original_numbers:
            self.board[i, j] = self.solution[i, j]
        self.solved = False
        self.solver = SudokuSolver(self.board, self.groups)

    def start_solving(self):
        if not self.solved:
            self.solver.start_solving()

    def solve_step_by_step(self):
        if self.solver.solving:
            if self.solver.solve_step_by_step():
                self.solved = True 