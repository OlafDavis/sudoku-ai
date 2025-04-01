import pygame
import numpy as np
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 540
CELL_SIZE = WINDOW_SIZE // 9
GRID_SIZE = 9
BUTTON_HEIGHT = 80  # Increased to accommodate two buttons

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)

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
        self.solving = False
        self.solve_delay = 0.05  # Delay between steps in seconds
        self.last_solve_time = 0
        self.filled_cells = []  # Keep track of cells we've filled during solving
        self.tried_numbers = {}  # Keep track of numbers tried for each cell
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
                            if num not in self.tried_numbers[(i, j)] and self.is_valid_move(num, (i, j), self.board):
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
            self.solved = True
            self.solving = False
            return True
        return False

    def start_solving(self):
        if not self.solved:
            self.solving = True
            self.last_solve_time = 0
            self.filled_cells = []  # Reset the filled cells list
            self.tried_numbers = {}  # Reset the tried numbers dictionary

    def stop_solving(self):
        self.solving = False
        self.filled_cells = []  # Clear the filled cells list
        self.tried_numbers = {}  # Clear the tried numbers dictionary

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
    
    # Create buttons
    button_width = 220
    button_spacing = 20
    total_buttons_width = button_width * 2 + button_spacing
    start_x = (WINDOW_SIZE - total_buttons_width) // 2
    button_y = WINDOW_SIZE + 5
    
    # Store original button positions
    reveal_button = pygame.Rect(start_x, button_y, button_width, 30)
    solve_button = pygame.Rect(start_x + button_width + button_spacing, button_y, button_width, 30)
    original_reveal_x = reveal_button.x
    original_solve_x = solve_button.x
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if buttons were clicked
                if reveal_button.collidepoint(event.pos):
                    if game.solved:
                        game.reset_puzzle()
                        # Restore original button positions
                        reveal_button.x = original_reveal_x
                        solve_button.x = original_solve_x
                    else:
                        game.reveal_solution()
                elif solve_button.collidepoint(event.pos):
                    if not game.solved:  # Only allow solving if not already solved
                        game.start_solving()
                else:
                    # Adjust y-coordinate for the game board click
                    adjusted_pos = (event.pos[0], event.pos[1])
                    if event.pos[1] < WINDOW_SIZE:  # Only handle clicks on the game board
                        game.handle_click(adjusted_pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                game.handle_key(event.key)
        
        # Handle step-by-step solving
        if game.solving:
            game.solve_step_by_step()
        
        screen.fill(WHITE)
        draw_board(screen, game)
        
        # Draw buttons
        if game.solved:
            # When solved, show only the Reset button in the center
            reveal_button.centerx = WINDOW_SIZE // 2
            reveal_text = "Reset"
            reveal_color = GREEN
            draw_button(screen, reveal_text, reveal_button, reveal_color)
        else:
            # When not solved, show both buttons
            reveal_text = "Reveal Solution"
            reveal_color = BLUE
            draw_button(screen, reveal_text, reveal_button, reveal_color)
            
            solve_text = "Solve Step by Step"
            draw_button(screen, solve_text, solve_button, PURPLE)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 