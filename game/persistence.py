import json
import os
from ui import Button
from ttt import TicTacToe
from rps import RPS
from connect4 import Connect4
from config import WIDTH, HEIGHT, BG_COLOR, WHITE, init_fonts, GRID_COLOR, BORDER_COLOR, X_COLOR, O_COLOR, HIGHLIGHT, MESSAGE_BG, C4_P1_COLOR, C4_P2_COLOR
from utils import valid_moves

def reset_q_table(filename):
    """
    Resets the Q-table by saving an empty dictionary to the specified file.
    Args:
        filename (str): The name of the JSON file to reset.
    Returns:
        str: A message indicating the result of the reset operation.
    """
    try:
        with open(filename, 'w') as f:
            json.dump({}, f)
        return f"Q-table {filename} has been reset."
    except Exception as e:
        return f"Error resetting Q-table {filename}: {str(e)}"

def load_q_table(filename):
    """
    Loads the Q-table from a JSON file.
    Args:
        filename (str): The name of the JSON file to load.
    Returns:
        dict: The loaded Q-table, or an empty dictionary if the file doesn't exist.
    """
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading Q-table {filename}: {str(e)}")
        return {}

def save_q_table(q_table, filename):
    """
    Saves the Q-table to a JSON file.
    Args:
        q_table (dict): The Q-table to save.
        filename (str): The name of the JSON file to save to.
    """
    try:
        with open(filename, 'w') as f:
            json.dump(q_table, f)
    except Exception as e:
        print(f"Error saving Q-table {filename}: {str(e)}")