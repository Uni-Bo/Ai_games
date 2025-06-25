import pygame
from ui import Button
from rps import RPS
from config import WIDTH, HEIGHT, BG_COLOR, WHITE, init_fonts, MESSAGE_BG

class RPSGameScene:
    def __init__(self, q_table):
        self.game = RPS(q_table)
        self.result = ""
        font_large, font_medium, font_small = init_fonts()
        self.font_large = font_large
        self.font_medium = font_medium
        self.font_small = font_small
        self.mode = None
        button_width = 100
        button_height = 50
        button_spacing = 20
        total_width = 3 * button_width + 2 * button_spacing
        start_x = (WIDTH - total_width) // 2
        start_y = HEIGHT // 2 + 50
        self.buttons = [
            Button(start_x, start_y, button_width, button_height, "Rock", font_small, lambda: self.play('rock')),
            Button(start_x + button_width + button_spacing, start_y, button_width, button_height, "Paper", font_small, lambda: self.play('paper')),
            Button(start_x + 2 * (button_width + button_spacing), start_y, button_width, button_height, "Scissors", font_small, lambda: self.play('scissors')),
            Button(50, HEIGHT - 70, 100, 50, "Back", font_medium, lambda: 'main_menu'),
            Button(WIDTH - 150, HEIGHT - 70, 100, 50, "Reset", font_medium, lambda: self.reset())
        ]

    def play(self, choice):
        if self.game and self.mode:
            ai_choice, outcome = self.game.play(choice, self.mode)
            if ai_choice is not None:
                outcome_text = {1: 'Win', 0: 'Tie', -1: 'Lose'}[outcome]
                self.result = f"You: {choice.capitalize()} vs AI: {ai_choice.capitalize()} -> You {outcome_text}!"
            else:
                self.result = "Invalid choice!"
        return None

    def reset(self):
        self.game.reset()
        self.result = ""
        return None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'main_menu'
        for button in self.buttons:
            result = button.check_click(event)
            if result is not None:
                return result
        return None

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BG_COLOR)
        title_surface = self.font_large.render("Rock Paper Scissors", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(title_surface, title_rect)
        score_surface = self.font_medium.render(f"Score You: {self.game.score[0]} | AI: {self.game.score[1]}", True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(score_surface, score_rect)
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            hover = button.rect.collidepoint(pos)
            button.draw(screen, hover)
        if self.result:
            result_surface = self.font_small.render(self.result, True, WHITE)
            result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            pygame.draw.rect(screen, MESSAGE_BG, result_rect.inflate(20, 20), border_radius=5)
            screen.blit(result_surface, result_rect)