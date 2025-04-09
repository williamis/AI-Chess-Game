from flask import Flask, render_template, request, jsonify
import chess
import ai

app = Flask(__name__)
board = chess.Board()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global board
    data = request.get_json()
    move_str = data["from"] + data["to"]
    if board.is_legal(chess.Move.from_uci(move_str)):
        board.push_uci(move_str)
        ai_move = ai.get_ai_move(board)
        board.push(ai_move)
        return jsonify({"valid": True, "fen": board.fen()})
    else:
        return jsonify({"valid": False, "fen": board.fen()})

if __name__ == "__main__":
    app.run(debug=True)
