from flask import Flask, render_template, request, jsonify, session
import chess
import ai
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def get_board():
    if 'fen' not in session:
        session['fen'] = chess.STARTING_FEN
    return chess.Board(session['fen'])

def save_board(board):
    session['fen'] = board.fen()

@app.route("/")
def index():
    session.pop('fen', None)
    return render_template("index.html")

@app.route("/reset", methods=["POST"])
def reset():
    session.pop('fen', None)
    return jsonify({"valid": True, "fen": chess.STARTING_FEN})

@app.route("/move", methods=["POST"])
def move():
    board = get_board()
    data = request.get_json()
    difficulty = int(data.get("difficulty", 2))
    move_str = data["from"] + data["to"]
    
    try:
        move = chess.Move.from_uci(move_str)
        
        # Sotilaan korotus
        piece = board.piece_at(move.from_square)
        if piece and piece.piece_type == chess.PAWN:
            if (board.turn == chess.WHITE and chess.square_rank(move.to_square) == 7) or \
               (board.turn == chess.BLACK and chess.square_rank(move.to_square) == 0):
                if not move.promotion:
                    move = chess.Move.from_uci(move_str + "q")

        if move in board.legal_moves:
            # Tallennetaan siirto tekstinä ennen suoritusta
            user_move_san = board.san(move)
            board.push(move)
            
            if board.is_game_over():
                save_board(board)
                return jsonify({
                    "valid": True, "fen": board.fen(), "user_move": user_move_san, 
                    "ai_move": None, "game_over": True, "status": board.result()
                })

            # AI:n vastaus
            ai_move_obj = ai.get_ai_move(board, depth=difficulty)
            ai_move_san = board.san(ai_move_obj)
            board.push(ai_move_obj)
            
            save_board(board)
            return jsonify({
                "valid": True, "fen": board.fen(), 
                "user_move": user_move_san, "ai_move": ai_move_san,
                "game_over": board.is_game_over(),
                "status": board.result() if board.is_game_over() else None
            })
        else:
            return jsonify({"valid": False, "error": "Laiton siirto!"})
            
    except Exception as e:
        return jsonify({"valid": False, "error": "Virhe siirron käsittelyssä."})

if __name__ == "__main__":
    app.run(debug=True)