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
        # Create 5 random pairs of adjacent cells that sum to 10
        possible_pairs = []
        # Generate all possible adjacent pairs
        for i in range(9):
            for j in range(9):
                # Check right
                if j < 8:
                    possible_pairs.append([(i, j), (i, j + 1)])
                # Check down
                if i < 8:
                    possible_pairs.append([(i, j), (i + 1, j)])
        
        # Randomly select pairs until we find 5 that sum to 10 in the solution
        selected_pairs = []
        random.shuffle(possible_pairs)
        
        for pair in possible_pairs:
            if len(selected_pairs) >= 5:
                break
                
            # Check if the numbers in these cells sum to 10
            num1 = self.solution[pair[0][0], pair[0][1]]
            num2 = self.solution[pair[1][0], pair[1][1]]
            
            if num1 + num2 == 10:
                selected_pairs.append(pair)
        
        # Store the pairs and their target sum
        self.groups = [(pair, 10) for pair in selected_pairs]

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