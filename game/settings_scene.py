import pygame
from ui import Button
from config import WIDTH, HEIGHT, BG_COLOR, WHITE, init_fonts, MESSAGE_BG
from persistence import reset_q_table

class SettingsScene:
    def __init__(self):
        font_large, font_medium, font_small = init_fonts()
        self.message = ""
        button_width = 300
        button_height = 50
        button_x = (WIDTH - button_width) // 2
        button_y_start = HEIGHT // 2 - 100
        button_spacing = 70

        self.buttons = [
            Button(button_x, button_y_start, button_width, button_height, "Reset Tic-Tac-Toe AI", font_medium, lambda: self.reset_ai('q_table_ttt.json')),
            Button(button_x, button_y_start + button_spacing, button_width, button_height, "Reset RPS AI", font_medium, lambda: self.reset_ai('q_table_rps.json')),
            Button(button_x, button_y_start + 2 * button_spacing, button_width, button_height, "Reset Connect 4 AI", font_medium, lambda: self.reset_ai('q_table_c4.json')),
            Button(50, HEIGHT - 70, 100, 50, "Back", font_medium, lambda: 'main_menu')
        ]
        self.title_surface = font_large.render("Settings", True, WHITE)
        self.title_rect = self.title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
        self.font_small = font_small

    def reset_ai(self, filename):
        self.message = reset_q_table(filename)
        return None

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            self.message = ""
        for button in self.buttons:
            result = button.check_click(event)
            if result:
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
        if self.message:
            message_surface = self.font_small.render(self.message, True, WHITE)
            message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            pygame.draw.rect(screen, MESSAGE_BG, message_rect.inflate(20, 10), border_radius=5)
            screen.blit(message_surface, message_rect)