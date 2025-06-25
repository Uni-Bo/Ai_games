import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, on_click=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.on_click = on_click
        self.text_surface = font.render(text, True, (255, 255, 255))

    def draw(self, screen, hover, button_color=(100, 100, 100), hover_color=(150, 150, 150)):
        color = hover_color if hover else button_color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.on_click:
                return self.on_click()
        return None