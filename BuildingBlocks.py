import pygame


def create_button(
    screen, message, x, y, width, height, default_color, hover_color=(200, 200, 200)
):
    """
    Create an interactive button in Pygame

    Parameters:
    - screen: pygame display surface
    - message: text to display on button
    - x, y: position coordinates
    - width, height: button dimensions
    - default_color: RGB tuple for button's normal color
    - hover_color: RGB tuple for button's hover color (optional)

    Returns:
    - bool: True if button is clicked
    """
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(x, y, width, height)

    # Check if mouse is hovering over button
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect)
        # Check for click
        if click[0] == 1:  # Left mouse button
            return True
    else:
        pygame.draw.rect(screen, default_color, button_rect)

    # Add text to button
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (0, 0, 0))  # Black text

    # Center text on button
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    return False


pygame.init()
screen = pygame.display.set_mode((800, 600))

running = True
while running:
    screen.fill((255, 255, 255))  # White background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create your button
    if create_button(screen, "Click Me!", 300, 250, 200, 50, (100, 200, 100)):
        print("Button was clicked!")
        # Add your button click actions here

    pygame.display.flip()

pygame.quit()
