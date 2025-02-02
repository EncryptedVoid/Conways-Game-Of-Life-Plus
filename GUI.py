import pygame
from Stage import Stage
import random
import time  # We'll use this for an alternative timing method

pygame.init()

# Constants for our grid (keeping your existing constants)
WINDOW_SIZE = (800, 800)
GRID_SIZE = 50
COLS = WINDOW_SIZE[0] // GRID_SIZE
ROWS = WINDOW_SIZE[1] // GRID_SIZE

# Add speed control constants
FRAME_RATE = 60  # How many frames per second to render
GENERATION_DELAY = 0.5  # Time between generations in seconds

stage = Stage(ROWS, COLS)

# Initialize random grid (keeping your existing initialization)
for row in range(ROWS):
    for col in range(COLS):
        stage.current_grid[row][col] = random.random() < 0.5

screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

# Add a variable to track the last generation time
last_generation_time = time.time()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # Update display
    pygame.display.flip()

    # Check if enough time has passed to generate the next generation
    current_time = time.time()
    if current_time - last_generation_time >= GENERATION_DELAY:
        stage.generate_next_grid()
        last_generation_time = current_time

    # Maintain frame rate
    clock.tick(FRAME_RATE)

pygame.quit()
