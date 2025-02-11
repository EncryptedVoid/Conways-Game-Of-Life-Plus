class Button:
    def __init__(self, x, y, width, height, text, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)

        # Base colors with alpha for transparency
        self.base_color = pygame.Color(255, 255, 255, 128)  # Semi-transparent white
        self.hover_color = pygame.Color(255, 255, 255, 180)  # More opaque white
        self.border_color = pygame.Color(255, 255, 255, 200)  # Nearly opaque white
        self.text_color = pygame.Color(255, 255, 255)  # Pure white
        self.glow_color = pygame.Color(200, 200, 255, 100)  # Light blue glow

        self.is_hovered = False
        self.corner_radius = 15  # Rounded corners radius

        # Create surfaces for the button
        self.normal_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.hover_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.glow_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)

        # Pre-render surfaces
        self._prepare_surfaces()

    def _prepare_surfaces(self):
        # Normal surface (non-hovered state)
        self._draw_rounded_rect(
            self.normal_surface,
            self.base_color,
            (0, 0, self.rect.width, self.rect.height),
            self.corner_radius,
        )

        # Add subtle gradient to normal surface
        self._add_gradient(self.normal_surface, 0.2)

        # Hover surface
        self._draw_rounded_rect(
            self.hover_surface,
            self.hover_color,
            (0, 0, self.rect.width, self.rect.height),
            self.corner_radius,
        )
        self._add_gradient(self.hover_surface, 0.3)

        # Glow surface
        glow_rect = pygame.Rect(10, 10, self.rect.width, self.rect.height)
        self._draw_rounded_rect(
            self.glow_surface, self.glow_color, glow_rect, self.corner_radius + 5
        )

    def _draw_rounded_rect(self, surface, color, rect, radius):
        """Draw a rounded rectangle with transparency"""
        rect = pygame.Rect(rect)

        # Draw the main rectangles
        pygame.draw.rect(surface, color, rect.inflate(-radius * 2, 0))
        pygame.draw.rect(surface, color, rect.inflate(0, -radius * 2))

        # Draw the corner circles
        for corner in [
            (rect.topleft, rect.topright),
            (rect.bottomleft, rect.bottomright),
        ]:
            for x, y in [
                (corner[0][0] + radius, corner[0][1] + radius),
                (corner[1][0] - radius, corner[1][1] + radius),
            ]:
                pygame.draw.circle(surface, color, (int(x), int(y)), radius)

    def _add_gradient(self, surface, intensity):
        """Add a subtle gradient effect"""
        gradient = pygame.Surface(
            (surface.get_width(), surface.get_height()), pygame.SRCALPHA
        )
        for y in range(surface.get_height()):
            alpha = int(255 * (1 - y / surface.get_height()) * intensity)
            gradient.fill((255, 255, 255, alpha), (0, y, surface.get_width(), 1))
        surface.blit(gradient, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    def draw(self, screen):
        # Draw glow effect if hovered
        if self.is_hovered:
            screen.blit(self.glow_surface, (self.rect.x - 10, self.rect.y - 10))
            current_surface = self.hover_surface
        else:
            current_surface = self.normal_surface

        # Draw button
        screen.blit(current_surface, self.rect)

        # Draw border
        pygame.draw.rect(
            screen, self.border_color, self.rect, 2, border_radius=self.corner_radius
        )

        # Draw text
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
