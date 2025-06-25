import pygame
from main_menu_scene import MainMenuScene
from settings_scene import SettingsScene
from mode_select_scene import ModeSelectScene
from ttt_game_scene import TTTGameScene
from rps_game_scene import RPSGameScene
from connect4_game_scene import Connect4GameScene
from config import WIDTH, HEIGHT
from persistence import load_q_table, save_q_table

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("AI Game Suite")
        self.q_table_ttt = load_q_table('q_table_ttt.json')
        self.q_table_rps = load_q_table('q_table_rps.json')
        self.q_table_c4 = load_q_table('q_table_c4.json')
        self.scenes = {
            'main_menu': MainMenuScene(),
            'settings': SettingsScene(),
            'ttt_select': ModeSelectScene('ttt'),
            'rps_select': ModeSelectScene('rps'),
            'c4_select': ModeSelectScene('c4'),
            'ttt_naive': TTTGameScene(self.q_table_ttt),
            'ttt_biassed': TTTGameScene(self.q_table_ttt),
            'ttt_minimax': TTTGameScene(self.q_table_ttt),
            'rps_naive': RPSGameScene(self.q_table_rps),
            'rps_biassed': RPSGameScene(self.q_table_rps),
            'rps_rl': RPSGameScene(self.q_table_rps),
            'c4_naive': Connect4GameScene(self.q_table_c4),
            'c4_biassed': Connect4GameScene(self.q_table_c4)
        }
        self.current_scene = self.scenes['main_menu']

    def quit_game(self):
        """
        Saves Q-tables and prepares the game for clean exit.
        """
        try:
            save_q_table(self.q_table_ttt, 'q_table_ttt.json')
            save_q_table(self.q_table_rps, 'q_table_rps.json')
            save_q_table(self.q_table_c4, 'q_table_c4.json')
        except Exception as e:
            print(f"Error saving Q-tables: {e}")

if __name__ == "__main__":
    import asyncio
    async def run_game():
        game = Game()
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.quit_game()
                    running = False
                    break
                next_scene_info = game.current_scene.handle_event(event)
                if next_scene_info is not None:
                    if isinstance(next_scene_info, tuple):
                        game_type, mode = next_scene_info
                        scene_key = f"{game_type}_{mode}"
                        game.current_scene = game.scenes[scene_key]
                        if hasattr(game.current_scene, 'mode'):
                            game.current_scene.mode = mode
                    elif next_scene_info in game.scenes:
                        game.current_scene = game.scenes[next_scene_info]
                    elif next_scene_info is None and hasattr(game.current_scene, 'should_quit') and game.current_scene.should_quit:
                        game.quit_game()
                        running = False
                        break

            if hasattr(game.current_scene, 'should_quit') and game.current_scene.should_quit:
                game.quit_game()
                running = False
                break

            game.current_scene.update()
            game.current_scene.draw(game.screen)
            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(1.0 / 60)
        pygame.quit()

    asyncio.run(run_game())