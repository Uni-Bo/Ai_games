import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
# --- Constants ---
GRID_SIZE = 3
CELL_SIZE = 100  # Cell size for Tic Tac Toe board
BOARD_SIZE = GRID_SIZE * CELL_SIZE # Total size of the Tic Tac Toe board
MARGIN = 30 # Margin around game elements from screen edges

# WIDTH and HEIGHT are initially set here but will be dynamically updated
# to full screen resolution in main.py.
WIDTH, HEIGHT = BOARD_SIZE + MARGIN * 2, BOARD_SIZE + 220
FPS = 60 # Frames per second

# --- Colors (RGB tuples) ---
BG_COLOR = (240, 240, 245)      # Light background
TEXT_COLOR = (20, 20, 30)       # Dark text
BUTTON_COLOR = (120, 160, 220)  # Softer blue for buttons
BUTTON_HOVER = (90, 130, 190)   # Darker blue on button hover
GRID_COLOR = (255, 255, 255)    # White for grid background
X_COLOR = (230, 50, 70)         # Red for 'X' marks
O_COLOR = (50, 115, 230)        # Blue for 'O' marks
HIGHLIGHT = (255, 255, 102)     # Brighter yellow for winning line/cells
MESSAGE_BG = (220, 220, 220)    # Light grey for message box background
BORDER_COLOR = (30, 30, 30)     # Dark grey/black for borders and lines
BLACK = (0, 0, 0)               # Pure black for general drawing

FONT_SMALL = "freesansbold.ttf" # Font file name for smaller text
FONT_LARGE = "freesansbold.ttf" # Font file name for larger text

# --- Q-learning Parameters ---
ALPHA = 0.2     # Learning rate (how much new information overrides old)
GAMMA = 0.95    # Discount factor (importance of future rewards)
EPSILON = 0.1   # Exploration rate (probability of choosing a random action)

# --- Tic Tac Toe Winning Combinations ---
# Defines all 8 possible winning lines for a 3x3 grid (row, col)
WIN_COMBOS = [
    [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)], # Rows
    [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)], # Columns
    [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]                       # Diagonals
]

# --- Rock Paper Scissors Choices and Outcomes ---
RPS_CHOICES = ['rock', 'paper', 'scissors']
# Dictionary mapping (player_choice, ai_choice) to outcome from player's perspective:
#  1: Player wins, 0: Tie, -1: AI wins
RPS_OUTCOMES = {
    ('rock', 'rock'): 0, ('rock', 'paper'): -1, ('rock', 'scissors'): 1,
    ('paper', 'rock'): 1, ('paper', 'paper'): 0, ('paper', 'scissors'): -1,
    ('scissors', 'rock'): -1, ('scissors', 'paper'): 1, ('scissors', 'scissors'): 0
}

# --- Utility Functions ---
def init_fonts():
    """
    Initializes Pygame fonts for large, medium, and small text sizes using the default font.
    Returns:
        tuple: Three Pygame font objects (font_large, font_medium, font_small).
    """
    pygame.font.init()
    font_large = pygame.font.Font(None, 48)  # Large font for titles
    font_medium = pygame.font.Font(None, 36)  # Medium font for buttons and scores
    font_small = pygame.font.Font(None, 24)  # Small font for messages
    return font_large, font_medium, font_small

def board_to_key(board):
    """
    Converts the Tic Tac Toe board state (list) to an immutable tuple.
    This is necessary for using board states as keys in a Q-table (dictionary).
    Args:
        board (list): The current 1D Tic Tac Toe board.
    Returns:
        tuple: An immutable representation of the board state.
    """
    return tuple(board)

def valid_moves(board):
    """
    Returns a list of valid (empty) positions on the Tic Tac Toe board.
    Args:
        board (list): The current 1D Tic Tac Toe board.
    Returns:
        list: A list of 0-indexed integers representing empty cells.
    """
    return [i for i, v in enumerate(board) if v == 0]

def check_win(board, player):
    """
    Checks if the given player has won the Tic Tac Toe game.
    Args:
        board (list): The current 1D Tic Tac Toe board (0 for empty, 1 for player 1, 2 for player 2).
        player (int): The player to check for a win (1 or 2).
    Returns:
        list: A list of (row, col) tuples forming the winning combination if player won, else None.
    """
    # Convert linear board to 2D for easier combo checking with WIN_COMBOS
    # Each inner list represents a row of the 3x3 board
    board_2d = [[board[r*GRID_SIZE+c] for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]
    for combo in WIN_COMBOS:
        # Check if all positions in the current winning combination are occupied by the player
        if all(board_2d[r][c] == player for r,c in combo):
            return combo # Return the winning combination if found
    return None # No winning combination found for the given player

