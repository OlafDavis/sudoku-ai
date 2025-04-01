import numpy as np
import pygame
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
        self.generate_puzzle()

    def generate_puzzle(self):
        self.board, self.solution, self.original_numbers = PuzzleGenerator.generate_puzzle()
        self.solver = SudokuSolver(self.board)
        self.solved = False

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
        self.solver = SudokuSolver(self.board)

    def start_solving(self):
        if not self.solved:
            self.solver.start_solving()

    def solve_step_by_step(self):
        if self.solver.solving:
            if self.solver.solve_step_by_step():
                self.solved = True 