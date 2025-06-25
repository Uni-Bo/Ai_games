import pygame
from ui import Button
from config import WIDTH, HEIGHT, BG_COLOR, WHITE, init_fonts

class ModeSelectScene:
    def __init__(self, game_type):
        self.game_type = game_type
        font_large, font_medium, _ = init_fonts()
        button_width = 200
        button_height = 50
        button_spacing = 20

        if game_type == 'ttt':
            modes = [("Easy (Naive)", 'naive'), ("Medium (Heuristic)", 'biassed'), ("Hard (Minimax)", 'minimax')]
        elif game_type == 'rps':
            modes = [("Easy (Naive)", 'naive'), ("Medium (Biased)", 'biassed'), ("Hard (RL)", 'rl')]
        elif game_type == 'c4':
            modes = [("Easy (Naive)", 'naive'), ("Medium (Heuristic)", 'biassed')]
        else:
            modes = []

        total_width = len(modes) * button_width + (len(modes) - 1) * button_spacing
        start_x = (WIDTH - total_width) // 2
        start_y = HEIGHT // 2

        self.buttons = []
        for i, (text, mode) in enumerate(modes):
            self.buttons.append(Button(start_x + i * (button_width + button_spacing), start_y, button_width, button_height, text, font_medium, lambda m=mode: (self.game_type, m)))

        back_button_x = (WIDTH - button_width) // 2
        self.buttons.append(Button(back_button_x, start_y + button_height + button_spacing, button_width, button_height, "Back", font_medium, lambda: 'main_menu'))

        self.title_surface = font_large.render(f"Select {self.game_type.upper()} Mode", True, WHITE)
        self.title_rect = self.title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    def handle_event(self, event):
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