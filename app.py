from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # ✅ IMPORTANT: allows frontend (GitHub Pages / localhost) to talk to backend


# ------------------ CORE LOGIC ------------------

def generate_fen(data):
    position = {
        f"{file}{rank}": None
        for rank in range(8, 0, -1)
        for file in "abcdefgh"
    }

    move = int(data["move"])

    def place_pieces(coords, piece):
        for sq in coords:
            sq = sq.lower()
            if sq not in position:
                return f"incorrect coordinate: {sq}"
            if position[sq] is not None:
                return f"square already occupied: {sq}"
            position[sq] = piece
        return None

    # ---- Kings ----
    kw = data["kw"].split()
    kb = data["kb"].split()

    if len(kw) != 1 or len(kb) != 1:
        return "invalid number of kings present"

    err = place_pieces(kw, "K")
    if err:
        return err

    err = place_pieces(kb, "k")
    if err:
        return err

    kwfile, kwrank = ord(kw[0][0]), int(kw[0][1])
    kbfile, kbrank = ord(kb[0][0]), int(kb[0][1])

    if abs(kwrank - kbrank) <= 1 and abs(kwfile - kbfile) <= 1:
        return "there should be at least one square between kings"

    # ---- Other Pieces ----
    piece_map = [
        ("qw", "Q"), ("qb", "q"),
        ("bw", "B"), ("bb", "b"),
        ("nw", "N"), ("nb", "n"),
        ("rw", "R"), ("rb", "r"),
    ]

    for key, piece in piece_map:
        if data.get(key):
            err = place_pieces(data[key].split(), piece)
            if err:
                return err

    # ---- Pawns ----
    forbidden = {
        "a1","b1","c1","d1","e1","f1","g1","h1",
        "a8","b8","c8","d8","e8","f8","g8","h8"
    }

    for key, piece in [("pw", "P"), ("pb", "p")]:
        if data.get(key):
            for sq in data[key].split():
                sq = sq.lower()
                if sq in forbidden:
                    return "pawn cannot be kept on first or last rank"
                err = place_pieces([sq], piece)
                if err:
                    return err

    # ---- Build FEN board ----
    fen_parts = []
    empty = 0
    values = list(position.values())

    for i in range(64):
        if values[i] is None:
            empty += 1
        else:
            if empty:
                fen_parts.append(str(empty))
                empty = 0
            fen_parts.append(values[i])

        if (i + 1) % 8 == 0:
            if empty:
                fen_parts.append(str(empty))
                empty = 0
            if i != 63:
                fen_parts.append("/")

    fen = "".join(fen_parts)

    fen += " w" if move == 1 else " b"

    castle = ""
    if data["castle"].get("K"): castle += "K"
    if data["castle"].get("Q"): castle += "Q"
    if data["castle"].get("k"): castle += "k"
    if data["castle"].get("q"): castle += "q"
    if castle == "":
        castle = "-"

    fen += " " + castle

    return fen


# ------------------ API ROUTE ------------------

@app.route("/generate_fen", methods=["POST"])
def generate():
    data = request.json

    result = generate_fen(data)

    if (
        "incorrect" in result
        or "invalid" in result
        or "pawn" in result
        or "square" in result
    ):
        return jsonify({"error": result}), 400

    lichess_url = "https://lichess.org/analysis/standard/" + result.replace(" ", "_")

    return jsonify({
        "fen": result,
        "lichess_url": lichess_url
    })


# ------------------ HEALTH CHECK (OPTIONAL BUT USEFUL) ------------------

@app.route("/", methods=["GET"])
def home():
    return "FEN backend is running"


# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
