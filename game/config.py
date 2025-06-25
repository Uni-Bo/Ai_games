import pygame
import sys

# Constants
FPS = 60
WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER = (150, 150, 150)
WHITE = (255, 255, 255)
GRID_COLOR = (50, 50, 50)
BORDER_COLOR = (200, 200, 200)
MESSAGE_BG = (80, 80, 80)
HIGHLIGHT = (255, 255, 0, 150) # Added alpha for transparency

# Tic-Tac-Toe Colors
X_COLOR = (255, 100, 100)
O_COLOR = (100, 100, 255)

# Connect 4 Colors
C4_P1_COLOR = (255, 0, 0)   # Red
C4_P2_COLOR = (255, 255, 0) # Yellow

# Font files
FONT_LARGE = "freesansbold.ttf"
FONT_SMALL = "freesansbold.ttf"

# Initialize fonts
def init_fonts():
    try:
        font_large = pygame.font.Font(FONT_LARGE, int(HEIGHT * 0.05))
        font_medium = pygame.font.Font(FONT_SMALL, int(HEIGHT * 0.035))
        font_small = pygame.font.Font(FONT_SMALL, int(HEIGHT * 0.025))
        return font_large, font_medium, font_small
    except FileNotFoundError:
        print("Error: Font file not found. Ensure 'freesansbold.ttf' is in the same directory.")
        pygame.quit()
        sys.exit(1)
    except pygame.error as e:
        print(f"Error initializing fonts: {e}")
        pygame.quit()
        sys.exit(1)
