import pygame
from game import Sudoku
from ui import (
    WINDOW_SIZE, BUTTON_HEIGHT, WHITE, BLUE, GREEN, PURPLE,
    draw_board, draw_button, create_buttons
)

def main():
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + BUTTON_HEIGHT))
    pygame.display.set_caption("Sudoku")
    
    # Initialize game
    game = Sudoku()
    running = True
    clock = pygame.time.Clock()
    
    # Create buttons
    reveal_button, solve_button, start_x = create_buttons()
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
                        game.handle_click(adjusted_pos, WINDOW_SIZE // 9)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                game.handle_key(event.key)
        
        # Handle step-by-step solving
        if game.solver.solving:
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