import pygame
import sys
import time
from Stage import Stage
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800 * 2
WINDOW_HEIGHT = 600 * 2
FPS = 60

GRID_SIZE = 25
COLS = WINDOW_WIDTH // GRID_SIZE
ROWS = WINDOW_HEIGHT // GRID_SIZE

FRAME_RATE = FPS  # How many frames per second to render
GENERATION_DELAY = 0.5  # Time between generations in seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

BUTTON_HEIGHT = 50
PLAY_BUTTON = pygame.Rect(
    WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - BUTTON_HEIGHT, 100, 40
)


class Button:
    def __init__(self, x, y, width, height, text, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = WHITE
        self.hover_color = GRAY
        self.text_color = BLACK
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Border

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False


class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.sliding = False

    def draw(self, screen):
        # Draw slider background
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        # Draw slider handle
        handle_pos = (
            self.rect.x
            + (self.value - self.min_val)
            / (self.max_val - self.min_val)
            * self.rect.width
        )
        handle_rect = pygame.Rect(handle_pos - 5, self.rect.y, 10, self.rect.height)
        pygame.draw.rect(screen, WHITE, handle_rect)

        # Draw text and value
        text_surface = self.font.render(f"{self.text}: {int(self.value)}", True, WHITE)
        text_rect = text_surface.get_rect(bottomleft=(self.rect.x, self.rect.y - 5))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.sliding = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.sliding = False

        elif event.type == pygame.MOUSEMOTION and self.sliding:
            # Update slider value based on mouse position
            relative_x = (
                min(max(event.pos[0], self.rect.left), self.rect.right) - self.rect.x
            )
            self.value = self.min_val + (self.max_val - self.min_val) * (
                relative_x / self.rect.width
            )
            return True
        return False


class Menu:

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game Menu")
        self.clock = pygame.time.Clock()

        # Button dimensions
        self.button_width = 200
        self.button_height = 50
        self.button_padding = 100  # Space between buttons

        # Calculate starting positions based on screen center
        center_x = WINDOW_WIDTH // 2
        start_y = WINDOW_HEIGHT // 3  # Start buttons 1/3 down screen

        # Center buttons horizontally by subtracting half their width
        button_x = center_x - (self.button_width // 2)

        # Create buttons with dynamic positioning
        self.start_button = Button(
            button_x, start_y, self.button_width, self.button_height, "Start Game"
        )

        self.settings_button = Button(
            button_x,
            start_y + self.button_height + self.button_padding,
            self.button_width,
            self.button_height,
            "Settings",
        )

        self.quit_button = Button(
            button_x,
            start_y + (self.button_height + self.button_padding) * 2,
            self.button_width,
            self.button_height,
            "Quit",
        )

        # Slider dimensions
        slider_width = 300
        slider_height = 20
        slider_x = center_x - (slider_width // 2)
        slider_start_y = start_y + (self.button_height + self.button_padding) * 3

        self.volume_slider = Slider(
            slider_x, slider_start_y, slider_width, slider_height, 0, 100, 50, "Volume"
        )

        self.brightness_slider = Slider(
            slider_x,
            slider_start_y + slider_height + self.button_padding,
            slider_width,
            slider_height,
            0,
            100,
            75,
            "Brightness",
        )

        self.in_settings = False
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.in_settings:
                # Handle settings menu events
                if self.volume_slider.handle_event(event):
                    print(f"Volume changed to: {self.volume_slider.value}")
                if self.brightness_slider.handle_event(event):
                    print(f"Brightness changed to: {self.brightness_slider.value}")

                # Back button
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.in_settings = False
            else:
                # Handle main menu events
                if self.start_button.handle_event(event):
                    print("Starting game...")
                    self.start_game()
                elif self.settings_button.handle_event(event):
                    self.in_settings = True
                elif self.quit_button.handle_event(event):
                    self.running = False

    def start_game(self):
        clock = pygame.time.Clock()
        last_generation_time = time.time()
        stage = Stage(ROWS, COLS)
        stage.current_grid = stage.blank_grid()
        simulation_running = False

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
                        not simulation_running
                        and mouse_pos[1] < WINDOW_HEIGHT - BUTTON_HEIGHT
                    ):
                        # Convert mouse position to grid coordinates
                        col = mouse_pos[0] // GRID_SIZE
                        row = mouse_pos[1] // GRID_SIZE
                        # Toggle cell state
                        stage.current_grid[row][col] = not stage.current_grid[row][col]

            # Clear screen and draw (keeping your existing drawing code)
            self.screen.fill((0, 0, 0))

            # Draw grid lines
            for x in range(0, WINDOW_WIDTH, GRID_SIZE):
                pygame.draw.line(
                    self.screen, (128, 128, 128), (x, 0), (x, WINDOW_HEIGHT)
                )
            for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
                pygame.draw.line(
                    self.screen, (128, 128, 128), (0, y), (WINDOW_WIDTH, y)
                )

            # Draw cells
            for row in range(ROWS):
                for col in range(COLS):
                    if stage.current_grid[row][col]:
                        rect_x = col * GRID_SIZE
                        rect_y = row * GRID_SIZE
                        pygame.draw.rect(
                            self.screen,
                            (255, 0, 0),
                            (rect_x, rect_y, GRID_SIZE, GRID_SIZE),
                        )

            # Draw the play/pause button
            button_color = (0, 255, 0) if simulation_running else (120, 120, 120)
            pygame.draw.rect(self.screen, button_color, PLAY_BUTTON)

            pygame.display.flip()

            # Only update generations if simulation is running
            if simulation_running:
                current_time = time.time()
                if current_time - last_generation_time >= GENERATION_DELAY:
                    stage.generate_next_grid()
                    last_generation_time = current_time

            clock.tick(FRAME_RATE)

        return

    def draw(self):
        self.screen.fill(BLACK)

        if self.in_settings:
            # Draw settings menu
            self.volume_slider.draw(self.screen)
            self.brightness_slider.draw(self.screen)

            # Draw back instruction
            font = pygame.font.Font(None, 24)
            back_text = font.render("Press ESC to go back", True, WHITE)
            self.screen.blit(back_text, (10, 10))
        else:
            # Draw main menu
            self.start_button.draw(self.screen)
            self.settings_button.draw(self.screen)
            self.quit_button.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    menu = Menu()
    menu.run()
    pygame.quit()
    sys.exit()
