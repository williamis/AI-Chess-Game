import chess
import random

PIECE_VALUES = {
    chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
}

PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

def evaluate_board(board):
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    
    score = 0
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            val = PIECE_VALUES[piece.piece_type]
            if piece.piece_type == chess.PAWN:
                val += PAWN_TABLE[sq if piece.color == chess.WHITE else chess.square_mirror(sq)]
            
            if piece.color == chess.WHITE: score += val
            else: score -= val
    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    moves = sorted(board.legal_moves, key=lambda m: board.is_capture(m), reverse=True)

    if maximizing_player:
        max_eval = -float('inf')
        for move in moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha: break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha: break
        return min_eval

def get_ai_move(board, depth=2):
    best_move = None
    best_value = float('inf')
    moves = sorted(board.legal_moves, key=lambda m: board.is_capture(m), reverse=True)
    
    for move in moves:
        board.push(move)
        val = minimax(board, depth - 1, -float('inf'), float('inf'), True)
        board.pop()
        if val < best_value:
            best_value = val
            best_move = move
    return best_move if best_move else random.choice(list(board.legal_moves))