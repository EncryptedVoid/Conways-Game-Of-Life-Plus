import pygame
from Stage import Stage
import random
import time
from pygame.locals import *

pygame.init()

# Keep your existing constants
WINDOW_SIZE = (800, 800)
GRID_SIZE = 25
COLS = WINDOW_SIZE[0] // GRID_SIZE
ROWS = WINDOW_SIZE[1] // GRID_SIZE

FRAME_RATE = 60  # How many frames per second to render
GENERATION_DELAY = 0.5  # Time between generations in seconds

# Add a variable to control simulation state
simulation_running = False

# Create a button area at the bottom
BUTTON_HEIGHT = 50
PLAY_BUTTON = pygame.Rect(
    WINDOW_SIZE[0] // 2 - 50, WINDOW_SIZE[1] - BUTTON_HEIGHT, 100, 40
)

stage = Stage(ROWS, COLS)
# Start with an empty grid instead of random
stage.current_grid = stage.blank_grid()

screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
last_generation_time = time.time()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if click is on the play button
            if PLAY_BUTTON.collidepoint(mouse_pos):
                simulation_running = not simulation_running
            # If click is in the grid area and simulation isn't running
            elif (
                not simulation_running and mouse_pos[1] < WINDOW_SIZE[1] - BUTTON_HEIGHT
            ):
                # Convert mouse position to grid coordinates
                col = mouse_pos[0] // GRID_SIZE
                row = mouse_pos[1] // GRID_SIZE
                # Toggle cell state
                stage.current_grid[row][col] = not stage.current_grid[row][col]

    # Clear screen and draw (keeping your existing drawing code)
    screen.fill((0, 0, 0))

    # Draw grid lines
    for x in range(0, WINDOW_SIZE[0], GRID_SIZE):
        pygame.draw.line(screen, (128, 128, 128), (x, 0), (x, WINDOW_SIZE[1]))
    for y in range(0, WINDOW_SIZE[1], GRID_SIZE):
        pygame.draw.line(screen, (128, 128, 128), (0, y), (WINDOW_SIZE[0], y))

    # Draw cells
    for row in range(ROWS):
        for col in range(COLS):
            if stage.current_grid[row][col]:
                rect_x = col * GRID_SIZE
                rect_y = row * GRID_SIZE
                pygame.draw.rect(
                    screen, (255, 0, 0), (rect_x, rect_y, GRID_SIZE, GRID_SIZE)
                )

    # Draw the play/pause button
    button_color = (0, 255, 0) if simulation_running else (120, 120, 120)
    pygame.draw.rect(screen, button_color, PLAY_BUTTON)

    pygame.display.flip()

    # Only update generations if simulation is running
    if simulation_running:
        current_time = time.time()
        if current_time - last_generation_time >= GENERATION_DELAY:
            stage.generate_next_grid()
            last_generation_time = current_time

    clock.tick(FRAME_RATE)

pygame.quit()
