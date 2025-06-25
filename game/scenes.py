import asyncio
import platform
import pygame
from main_menu_scene import MainMenuScene
from settings_scene import SettingsScene
from mode_select_scene import ModeSelectScene
from ttt_game_scene import TTTGameScene
from rps_game_scene import RPSGameScene
from connect4_game_scene import Connect4GameScene
from config import WIDTH, HEIGHT, FPS
from persistence import load_q_table, save_q_table

class SceneManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("AI Game Suite")
        self.clock = pygame.time.Clock()
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
        self.running = True

    async def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                    return
                next_scene_info = self.current_scene.handle_event(event)
                if next_scene_info is not None:
                    if isinstance(next_scene_info, tuple):
                        game_type, mode = next_scene_info
                        scene_key = f"{game_type}_{mode}"
                        self.current_scene = self.scenes[scene_key]
                        if hasattr(self.current_scene, 'mode'):
                            self.current_scene.mode = mode
                    elif next_scene_info in self.scenes:
                        self.current_scene = self.scenes[next_scene_info]
                    elif next_scene_info is None and hasattr(self.current_scene, 'should_quit') and self.current_scene.should_quit:
                        self.quit_game()
                        return

            # Check should_quit flag for MainMenuScene
            if isinstance(self.current_scene, MainMenuScene) and self.current_scene.should_quit:
                self.quit_game()
                return

            self.current_scene.update()
            self.current_scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
            await asyncio.sleep(1.0 / FPS)

    def quit_game(self):
        """
        Saves Q-tables and quits the game cleanly.
        """
        try:
            save_q_table(self.q_table_ttt, 'q_table_ttt.json')
            save_q_table(self.q_table_rps, 'q_table_rps.json')
            save_q_table(self.q_table_c4, 'q_table_c4.json')
        except Exception as e:
            print(f"Error saving Q-tables: {e}")
        pygame.quit()
        self.running = False

if platform.system() == "Emscripten":
    scene_manager = SceneManager()
    asyncio.ensure_future(scene_manager.run())
else:
    if __name__ == "__main__":
        scene_manager = SceneManager()
        asyncio.run(scene_manager.run())