import chess
import random

def get_ai_move(board):
    legal_moves = list(board.legal_moves)
    return random.choice(legal_moves)
