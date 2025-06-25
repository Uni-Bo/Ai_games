import pygame
from ui import Button
from ttt import TicTacToe
from config import WIDTH, HEIGHT, BG_COLOR, WHITE, GRID_COLOR, BORDER_COLOR, X_COLOR, O_COLOR, HIGHLIGHT, MESSAGE_BG
from utils import init_fonts

class TTTGameScene:
    def __init__(self, q_table):
        self.game = TicTacToe(q_table)
        self.cell_size = 100
        self.grid_x = (WIDTH - 3 * self.cell_size) // 2
        self.grid_y = (HEIGHT - 3 * self.cell_size) // 2
        self.message = ""
        self.message_timer = 0
        self.message_duration = 2000  # 2 seconds in milliseconds
        self.highlight = []
        font_large, font_medium, font_small = init_fonts()
        self.font_medium = font_medium
        self.font_small = font_small
        self.mode = None
        self.buttons = [
            Button(50, HEIGHT - 70, 100, 50, "Back", font_medium, lambda: 'main_menu'),
            Button(WIDTH - 150, HEIGHT - 70, 100, 50, "Reset", font_medium, lambda: self.reset())
        ]

    def reset(self):
        self.game.reset()
        self.message = ""
        self.message_timer = 0
        self.highlight = []
        return None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'main_menu'
        for button in self.buttons:
            result = button.check_click(event)
            if result is not None:
                return result
        if event.type == pygame.MOUSEBUTTONDOWN and not self.message:
            x, y = event.pos
            col = (x - self.grid_x) // self.cell_size
            row = (y - self.grid_y) // self.cell_size
            pos = row * 3 + col
            if 0 <= col < 3 and 0 <= row < 3:
                if self.game.board[pos] == 0:
                    res = self.game.play(pos)
                    if res:
                        self.handle_game_end(res)
                    else:
                        ai_move = self.game.ai_move(self.mode)
                        if ai_move is not None:
                            res2 = self.game.play(ai_move)
                            if res2:
                                self.handle_game_end(res2)
                else:
                    self.message = "Invalid Move: Cell not empty!"
                    self.message_timer = pygame.time.get_ticks()
        return None

    def handle_game_end(self, result):
        player_won, combo = result
        self.highlight = combo if combo else []
        if player_won == 0:
            self.message = "It's a Draw!"
        else:
            self.message = f"{'You' if player_won == 1 else 'AI'} Won!"
            if player_won == 1:
                self.game.score[0] += 1
            else:
                self.game.score[1] += 1
        self.message_timer = pygame.time.get_ticks()
        self.game.new_round()

    def update(self):
        if self.message and (pygame.time.get_ticks() - self.message_timer > self.message_duration):
            self.message = ""
            self.message_timer = 0
            self.highlight = []

    def draw(self, screen):
        screen.fill(BG_COLOR)
        score_surface = self.font_medium.render(f"Score: You {self.game.score[0]} | AI {self.game.score[1]}", True, WHITE)
        score_rect = scoreSscore_rect = score_surface.get_rect(center=(WIDTH // 2, self.grid_y - 50))
        screen.blit(score_surface, score_rect)

        pygame.draw.rect(screen, GRID_COLOR, (self.grid_x, self.grid_y, 3 * self.cell_size, 3 * self.cell_size), border_radius=10)
        pygame.draw.rect(screen, BORDER_COLOR, (self.grid_x, self.grid_y, 3 * self.cell_size, 3 * self.cell_size), 5, border_radius=10)
        for i in range(1, 3):
            pygame.draw.line(screen, BORDER_COLOR, (self.grid_x + i * self.cell_size, self.grid_y),
                             (self.grid_x + i * self.cell_size, self.grid_y + 3 * self.cell_size), 3)
            pygame.draw.line(screen, BORDER_COLOR, (self.grid_x, self.grid_y + i * self.cell_size),
                             (self.grid_x + 3 * self.cell_size, self.grid_y + i * self.cell_size), 3)

        for idx, val in enumerate(self.game.board):
            x0 = self.grid_x + (idx % 3) * self.cell_size
            y0 = self.grid_y + (idx // 3) * self.cell_size
            padding = self.cell_size // 6
            if val == 1:
                pygame.draw.line(screen, X_COLOR, (x0 + padding, y0 + padding),
                                 (x0 + self.cell_size - padding, y0 + self.cell_size - padding), 8)
                pygame.draw.line(screen, X_COLOR, (x0 + self.cell_size - padding, y0 + padding),
                                 (x0 + padding, y0 + self.cell_size - padding), 8)
            elif val == 2:
                pygame.draw.circle(screen, O_COLOR, (x0 + self.cell_size // 2, y0 + self.cell_size // 2),
                                   self.cell_size // 2 - 10, 8)

        for r, c in self.highlight:
            pygame.draw.rect(screen, HIGHLIGHT, (self.grid_x + c * self.cell_size + 2,
                                                 self.grid_y + r * self.cell_size + 2, self.cell_size - 4, self.cell_size - 4), 6, border_radius=5)

        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            hover = button.rect.collidepoint(pos)
            button.draw(screen, hover)

        if self.message:
            message_surface = self.font_small.render(self.message, True, WHITE)
            message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            pygame.draw.rect(screen, MESSAGE_BG, message_rect.inflate(20, 10), border_radius=5)
            screen.blit(message_surface, message_rect)