import pygame
from ui import Button
from config import WIDTH, HEIGHT, BG_COLOR, WHITE, init_fonts

class MainMenuScene:
    def __init__(self):
        font_large, font_medium, _ = init_fonts()
        button_width = 250
        button_height = 50
        button_x = (WIDTH - button_width) // 2
        button_y_start = HEIGHT // 2 - 150
        button_spacing = 70

        self.buttons = [
            Button(button_x, button_y_start, button_width, button_height, "Tic-Tac-Toe", font_medium, lambda: 'ttt_select'),
            Button(button_x, button_y_start + button_spacing, button_width, button_height, "Rock-Paper-Scissors", font_medium, lambda: 'rps_select'),
            Button(button_x, button_y_start + 2 * button_spacing, button_width, button_height, "Connect 4", font_medium, lambda: 'c4_select'),
            Button(button_x, button_y_start + 3 * button_spacing, button_width, button_height, "Settings", font_medium, lambda: 'settings'),
            Button(WIDTH - 120, HEIGHT - 70, 100, 50, "Quit", font_medium, lambda: self.quit_app())
        ]
        self.title_surface = font_large.render("AI Game Suite", True, WHITE)
        self.title_rect = self.title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 220))
        self.should_quit = False

    def quit_app(self):
        """
        Signals the application to close by setting a quit flag.
        """
        self.should_quit = True
        return None

    def handle_event(self, event):
        for button in self.buttons:
            result = button.check_click(event)
            if result is not None:
                return result
        return None

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BG_COLOR)
        screen.blit(self.title_surface, self.title_rect)
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            hover = button.rect.collidepoint(pos)
            button.draw(screen, hover)