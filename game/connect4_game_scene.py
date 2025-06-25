import pygame
from ui import Button
from connect4 import Connect4
from config import WIDTH, HEIGHT, BG_COLOR, WHITE, GRID_COLOR, BORDER_COLOR, C4_P1_COLOR, C4_P2_COLOR, HIGHLIGHT, MESSAGE_BG
from utils import init_fonts

class Connect4GameScene:
    def __init__(self, q_table):
        self.game = Connect4(q_table)
        self.cell_size = 70
        self.grid_width = 7 * self.cell_size
        self.grid_height = 6 * self.cell_size
        self.grid_x = (WIDTH - self.grid_width) // 2
        self.grid_y = (HEIGHT - self.grid_height) // 2 + 20
        self.message = ""
        self.highlight = []
        self.mode = None
        font_large, font_medium, font_small = init_fonts()
        self.font_medium = font_medium
        self.font_small = font_small
        self.buttons = [
            Button(50, HEIGHT - 70, 100, 50, "Back", font_medium, lambda: 'main_menu'),
            Button(WIDTH - 150, HEIGHT - 70, 100, 50, "Reset", font_medium, lambda: self.reset())
        ]

    def reset(self):
        self.game.reset()
        self.message = ""
        self.highlight = []
        return None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'main_menu'
        for button in self.buttons:
            result = button.check_click(event)
            if result is not None:
                return result
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, _ = event.pos
            if self.grid_x < x < self.grid_x + self.grid_width:
                col = (x - self.grid_x) // self.cell_size
                if self.game.is_valid_location(col):
                    if self.game.game_over:
                        self.game.new_round()
                        self.message = ""
                        self.highlight = []
                    res = self.game.play(col)
                    if res:
                        self.handle_game_end(res)
                    else:
                        ai_move = self.game.ai_move(self.mode)
                        if ai_move is not None:
                            res2 = self.game.play(ai_move)
                            if res2:
                                self.handle_game_end(res2)
                else:
                    self.message = "Invalid Move: Column is full!"
        return None

    def handle_game_end(self, result):
        player_won, combo = result
        self.highlight = combo if combo else []
        if player_won == 0:
            self.message = "It's a Draw! Click a column to play again."
        else:
            self.message = f"{'You' if player_won == 1 else 'AI'} Won! Click a column to play again."
            if player_won == 1:
                self.game.score[0] += 1
            else:
                self.game.score[1] += 1

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BG_COLOR)
        score_surface = self.font_medium.render(f"Score: You {self.game.score[0]} | AI {self.game.score[1]}", True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, self.grid_y - 40))
        screen.blit(score_surface, score_rect)

        pygame.draw.rect(screen, GRID_COLOR, (self.grid_x, self.grid_y, self.grid_width, self.grid_height), border_radius=10)

        for r in range(6):
            for c in range(7):
                color = BG_COLOR
                if self.game.board[r][c] == 1:
                    color = C4_P1_COLOR
                elif self.game.board[r][c] == 2:
                    color = C4_P2_COLOR
                pygame.draw.circle(screen, color, (self.grid_x + c * self.cell_size + self.cell_size // 2,
                                                   self.grid_y + r * self.cell_size + self.cell_size // 2), self.cell_size // 2 - 5)

        for r, c in self.highlight:
            pygame.draw.circle(screen, HIGHLIGHT, (self.grid_x + c * self.cell_size + self.cell_size // 2,
                                                   self.grid_y + r * self.cell_size + self.cell_size // 2), self.cell_size // 2 - 5, 5)

        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            hover = button.rect.collidepoint(pos)
            button.draw(screen, hover)

        if self.message:
            message_surface = self.font_small.render(self.message, True, WHITE)
            message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            pygame.draw.rect(screen, MESSAGE_BG, message_rect.inflate(20, 10), border_radius=5)
            screen.blit(message_surface, message_rect)