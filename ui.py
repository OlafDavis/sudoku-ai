import pygame

# Constants
WINDOW_SIZE = 540
CELL_SIZE = WINDOW_SIZE // 9
GRID_SIZE = 9
BUTTON_HEIGHT = 80

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (200, 230, 255)  # New color for current cell highlight
LIGHT_RED = (255, 200, 200)  # New color for group highlighting

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
    
    # Draw groups
    for group, target_sum in game.groups:
        # Draw light red background for the group
        for row, col in group:
            pygame.draw.rect(screen, LIGHT_RED, 
                           (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Draw target sum in the middle of the group
        font = pygame.font.Font(None, 24)
        text = font.render(str(target_sum), True, RED)
        # Calculate center position between the two cells
        x = (group[0][1] + group[1][1]) * CELL_SIZE // 2
        y = (group[0][0] + group[1][0]) * CELL_SIZE // 2
        text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
        screen.blit(text, text_rect)
    
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
    
    # Draw current cell being examined by solver
    if game.solver and game.solver.current_cell:
        row, col = game.solver.current_cell
        pygame.draw.rect(screen, LIGHT_BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_button(screen, text, rect, color):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    return rect

def create_buttons():
    button_width = 220
    button_spacing = 20
    total_buttons_width = button_width * 2 + button_spacing
    start_x = (WINDOW_SIZE - total_buttons_width) // 2
    button_y = WINDOW_SIZE + 5
    
    reveal_button = pygame.Rect(start_x, button_y, button_width, 30)
    solve_button = pygame.Rect(start_x + button_width + button_spacing, button_y, button_width, 30)
    
    return reveal_button, solve_button, start_x 