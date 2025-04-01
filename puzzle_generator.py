import numpy as np
import random

class PuzzleGenerator:
    @staticmethod
    def generate_solution():
        # Generate a valid Sudoku solution
        board = np.zeros((9, 9), dtype=int)
        numbers = list(range(1, 10))
        
        def is_valid(num, pos):
            row, col = pos
            # Check row
            if num in board[row]:
                return False
            # Check column
            if num in board[:, col]:
                return False
            # Check 3x3 box
            box_row, box_col = 3 * (row // 3), 3 * (col // 3)
            if num in board[box_row:box_row+3, box_col:box_col+3]:
                return False
            return True

        def solve():
            for i in range(9):
                for j in range(9):
                    if board[i, j] == 0:
                        random.shuffle(numbers)
                        for num in numbers:
                            if is_valid(num, (i, j)):
                                board[i, j] = num
                                if solve():
                                    return True
                                board[i, j] = 0
                        return False
            return True

        solve()
        return board

    @staticmethod
    def has_unique_solution(board):
        # Check if the puzzle has a unique solution
        solutions = []
        
        def is_valid_move(num, pos, board):
            row, col = pos
            # Check row
            if num in board[row]:
                return False
            # Check column
            if num in board[:, col]:
                return False
            # Check 3x3 box
            box_row, box_col = 3 * (row // 3), 3 * (col // 3)
            if num in board[box_row:box_row+3, box_col:box_col+3]:
                return False
            return True

        def solve(board):
            for i in range(9):
                for j in range(9):
                    if board[i, j] == 0:
                        for num in range(1, 10):
                            if is_valid_move(num, (i, j), board):
                                board[i, j] = num
                                solve(board)
                                board[i, j] = 0
                        return
            solutions.append(board.copy())
        
        solve(board.copy())
        return len(solutions) == 1

    @staticmethod
    def generate_puzzle():
        # Generate a solved Sudoku puzzle
        solution = PuzzleGenerator.generate_solution()
        board = solution.copy()
        
        # Remove some numbers to create the puzzle
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        # Remove numbers while ensuring unique solution
        for i, j in cells:
            if len(cells) > 40:  # Keep at least 41 numbers
                temp = board[i, j]
                board[i, j] = 0
                
                # Check if solution is unique
                if not PuzzleGenerator.has_unique_solution(board):
                    board[i, j] = temp
                else:
                    cells.remove((i, j))
        
        # Store original numbers
        original_numbers = {(i, j) for i in range(9) for j in range(9) if board[i, j] != 0}
        
        return board, solution, original_numbers 