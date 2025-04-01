import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 540
CELL_SIZE = WINDOW_SIZE // 9
GRID_SIZE = 9
BUTTON_HEIGHT = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + BUTTON_HEIGHT))
pygame.display.set_caption("Sudoku")

class Sudoku:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        self.solution = np.zeros((9, 9), dtype=int)
        self.selected = None
        self.original_numbers = set()
        self.solved = False
        self.generate_puzzle()

    def generate_puzzle(self):
        # Generate a solved Sudoku puzzle
        self.solution = self.generate_solution()
        self.board = self.solution.copy()
        
        # Remove some numbers to create the puzzle
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        # Remove numbers while ensuring unique solution
        for i, j in cells:
            if len(cells) > 40:  # Keep at least 41 numbers
                temp = self.board[i, j]
                self.board[i, j] = 0
                
                # Check if solution is unique
                if not self.has_unique_solution():
                    self.board[i, j] = temp
                else:
                    cells.remove((i, j))
        
        # Store original numbers
        self.original_numbers = {(i, j) for i in range(9) for j in range(9) if self.board[i, j] != 0}

    def generate_solution(self):
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

    def has_unique_solution(self):
        # Check if the puzzle has a unique solution
        solutions = []
        
        def solve(board):
            for i in range(9):
                for j in range(9):
                    if board[i, j] == 0:
                        for num in range(1, 10):
                            if self.is_valid_move(num, (i, j), board):
                                board[i, j] = num
                                solve(board)
                                board[i, j] = 0
                        return
            solutions.append(board.copy())
        
        solve(self.board.copy())
        return len(solutions) == 1

    def is_valid_move(self, num, pos, board):
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

    def handle_click(self, pos):
        x, y = pos
        if 0 <= x < WINDOW_SIZE and 0 <= y < WINDOW_SIZE:
            row = y // CELL_SIZE
            col = x // CELL_SIZE
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
            if self.is_valid_move(num, (row, col), self.board):
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

def draw_board(screen, game):
    # Draw grid lines
    for i in range(10):
        # Vertical lines
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE))
        # Horizontal lines
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE))
    
    # Draw thicker lines for 3x3 boxes
    for i in range(0, 10, 3):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), 2)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), 2)
    
    # Draw numbers
    font = pygame.font.Font(None, 40)
    for i in range(9):
        for j in range(9):
            if game.board[i, j] != 0:
                color = BLUE if (i, j) in game.original_numbers else BLACK
                text = font.render(str(game.board[i, j]), True, color)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2,
                                                i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)
    
    # Draw selected cell
    if game.selected:
        row, col = game.selected
        pygame.draw.rect(screen, RED, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

def draw_button(screen, text, rect, color):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    return rect

def main():
    game = Sudoku()
    running = True
    clock = pygame.time.Clock()
    
    # Create reveal button
    button_width = 180
    button_x = (WINDOW_SIZE - button_width) // 2
    button_y = WINDOW_SIZE + 5
    reveal_button = pygame.Rect(button_x, button_y, button_width, 30)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if reveal button was clicked
                if reveal_button.collidepoint(event.pos):
                    if game.solved:
                        game.reset_puzzle()
                    else:
                        game.reveal_solution()
                else:
                    # Adjust y-coordinate for the game board click
                    adjusted_pos = (event.pos[0], event.pos[1])
                    if event.pos[1] < WINDOW_SIZE:  # Only handle clicks on the game board
                        game.handle_click(adjusted_pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                game.handle_key(event.key)
        
        screen.fill(WHITE)
        draw_board(screen, game)
        
        # Draw reveal solution button
        button_text = "Reset" if game.solved else "Reveal Solution"
        button_color = GREEN if game.solved else BLUE
        draw_button(screen, button_text, reveal_button, button_color)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 