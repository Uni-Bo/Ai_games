import asyncio
import pygame
from game import Game
from config import WIDTH, HEIGHT, FPS

async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI Game Suite")
    clock = pygame.time.Clock()
    game = Game()
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
        game.current_scene.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())