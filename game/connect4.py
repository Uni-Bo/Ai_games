import random

# Constants for Connect 4
ROWS = 6
COLS = 7

class Connect4:
    """
    Implements the Connect 4 game logic.
    Supports player moves and AI moves (naive, biased).
    """
    def __init__(self, qtable=None): # qtable is a placeholder for a future RL agent
        self.board = [[0] * COLS for _ in range(ROWS)] # 0: empty, 1: player 1, 2: player 2 (AI)
        self.current = 1      # Current player: 1 for human, 2 for AI
        self.qtable = qtable
        self.game_over = False
        self.score = [0, 0]   # [Player 1 Score, Player 2 (AI) Score]

    def reset(self):
        """Resets the game board, state, and score for a new game."""
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.current = 1
        self.game_over = False
        self.score = [0, 0]

    def new_round(self):
        """Resets the board and state for a new round, preserving the score."""
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.current = 1
        self.game_over = False

    def play(self, col):
        """
        Processes a player's move by dropping a piece in a column.
        Args:
            col (int): The column (0-6) where the player wants to move.
        Returns:
            tuple or None:
                - (player, win_combo) if a player wins.
                - (0, None) for a draw.
                - None if the game continues.
        """
        if self.game_over or not self.is_valid_location(col):
            return None

        row = self.get_next_open_row(col)
        self.board[row][col] = self.current

        win_combo = self.check_win(self.current)
        if win_combo:
            self.game_over = True
            return (self.current, win_combo)

        if all(self.board[0][c] != 0 for c in range(COLS)): # Board is full
            self.game_over = True
            return (0, None) # It's a draw

        self.current = 3 - self.current # Switch player
        return None

    def is_valid_location(self, col):
        """Checks if a column has an open spot."""
        return self.board[0][col] == 0

    def get_next_open_row(self, col):
        """Finds the lowest open row in a given column."""
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == 0:
                return r
        return None

    def check_win(self, player):
        """
        Checks the entire board for a winning combination for the given player.
        Returns:
            list: A list of (row, col) tuples for the winning line, else None.
        """
        # Check horizontal locations for a win
        for c in range(COLS - 3):
            for r in range(ROWS):
                if all(self.board[r][c+i] == player for i in range(4)):
                    return [(r, c+i) for i in range(4)]
        # Check vertical locations for a win
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(self.board[r+i][c] == player for i in range(4)):
                    return [(r+i, c) for i in range(4)]
        # Check positively sloped diagonals
        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if all(self.board[r+i][c+i] == player for i in range(4)):
                    return [(r+i, c+i) for i in range(4)]
        # Check negatively sloped diagonals
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if all(self.board[r-i][c+i] == player for i in range(4)):
                    return [(r-i, c+i) for i in range(4)]
        return None

    def valid_moves(self):
        """Returns a list of columns that are not full."""
        return [c for c in range(COLS) if self.is_valid_location(c)]

    def ai_move(self, mode):
        """
        Determines the AI's move based on the selected mode.
        Args:
            mode (str): The AI difficulty ('naive', 'biassed').
        Returns:
            int: The chosen column for the AI's move.
        """
        moves = self.valid_moves()
        if not moves:
            return None

        if mode == 'naive':
            return random.choice(moves)
        
        elif mode == 'biassed':
            # Check if AI can win in the next move
            for col in moves:
                row = self.get_next_open_row(col)
                self.board[row][col] = 2 # Try the move for AI
                if self.check_win(2):
                    self.board[row][col] = 0 # Undo move
                    return col
                self.board[row][col] = 0 # Undo move
            
            # Check if player can win in the next move, and block them
            for col in moves:
                row = self.get_next_open_row(col)
                self.board[row][col] = 1 # Try the move for player
                if self.check_win(1):
                    self.board[row][col] = 0 # Undo move
                    return col
                self.board[row][col] = 0 # Undo move

            # Otherwise, prefer the center column
            center_col = COLS // 2
            if center_col in moves:
                return center_col
            
            # As a fallback, take a random valid move
            return random.choice(moves)
            
        return random.choice(moves) # Default for any other mode
