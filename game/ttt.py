import random
from utils import board_to_key, valid_moves, check_win

class TicTacToe:
    """
    Implements the Tic Tac Toe game logic.
    Supports player moves and AI moves (naive, biassed, minimax).
    """
    def __init__(self, qtable):
        self.board = [0] * 9  # 0: empty, 1: player X, 2: player O (AI)
        self.current = 1      # Current player: 1 for human, 2 for AI
        self.qtable = qtable  # Q-table for RL agent (not used by minimax)
        self.game_over = False
        self.score = [0, 0]   # [Player X (You) Score, Player O (AI) Score]

    def reset(self):
        self.board = [0] * 9
        self.current = 1
        self.game_over = False
        self.score = [0, 0]

    def new_round(self):
        self.board = [0] * 9
        self.current = 1
        self.game_over = False

    def play(self, pos):
        if self.game_over or self.board[pos] != 0 or not (0 <= pos < 9):
            return None

        self.board[pos] = self.current
        win = check_win(self.board, self.current)

        if win:
            self.game_over = True
            return (self.current, win)
        if not valid_moves(self.board):
            self.game_over = True
            return (0, None)

        self.current = 3 - self.current
        return None

    def _minimax(self, board, depth, is_maximizing):
        """
        Minimax algorithm to determine the best move.
        Args:
            board (list): The current board state.
            depth (int): The current depth of the recursion.
            is_maximizing (bool): True if finding the max score, False for min.
        Returns:
            int: The heuristic value of the board state.
        """
        # Terminal state checks
        if check_win(board, 2):  # AI (O, maximizing player) wins
            return 10 - depth
        if check_win(board, 1):  # Human (X, minimizing player) wins
            return depth - 10
        if not valid_moves(board):  # Draw
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for move in valid_moves(board):
                board[move] = 2  # AI's move
                score = self._minimax(board, depth + 1, False)
                board[move] = 0  # Undo move
                best_score = max(score, best_score)
            return best_score
        else:  # Minimizing player
            best_score = float('inf')
            for move in valid_moves(board):
                board[move] = 1  # Player's move
                score = self._minimax(board, depth + 1, True)
                board[move] = 0  # Undo move
                best_score = min(score, best_score)
            return best_score

    def ai_move(self, mode):
        moves = valid_moves(self.board)
        if not moves:
            return None

        if mode == 'naive':
            return random.choice(moves)
        
        elif mode == 'biassed':
            # Heuristic: Check for win, then block, then take center
            for target_player in [2, 1]:  # First check for AI win (2), then player block (1)
                for m in moves:
                    self.board[m] = target_player
                    if check_win(self.board, target_player):
                        self.board[m] = 0
                        return m
                    self.board[m] = 0
            return 4 if 4 in moves else random.choice(moves)

        elif mode == 'minimax':  # Unbeatable AI
            best_score = -float('inf')
            best_move = None
            for move in moves:
                self.board[move] = 2  # Try a move for the AI
                # Start recursion for the minimizing player (human)
                score = self._minimax(list(self.board), 0, False)
                self.board[move] = 0  # Undo the move
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_move

        return random.choice(moves) # Fallback
