from flask import Flask, request, jsonify

app = Flask(__name__)

games = {}

choices = ["rock", "paper", "scissors"]

def winner(p1, p2):
    if p1 == p2:
        return "draw"
    if (p1 == "rock" and p2 == "scissors") or \
       (p1 == "scissors" and p2 == "paper") or \
       (p1 == "paper" and p2 == "rock"):
        return "p1"
    return "p2"


# ایجاد یا ورود به بازی
@app.route("/join", methods=["POST"])
def join():
    data = request.json
    game_id = data["game_id"]
    player = data["player"]

    if game_id not in games:
        games[game_id] = {}

    games[game_id][player] = None

    return jsonify({
        "status": "joined",
        "game_id": game_id,
        "players": list(games[game_id].keys())
    })


# ثبت انتخاب بازیکن
@app.route("/play", methods=["POST"])
def play():
    data = request.json

    game_id = data["game_id"]
    player = data["player"]
    choice = data["choice"]

    if game_id not in games:
        return jsonify({"status": "error", "msg": "game not found"})

    if choice not in choices:
        return jsonify({"status": "error", "msg": "invalid choice"})

    games[game_id][player] = choice

    # هنوز 2 نفر کامل نشده
    if len(games[game_id]) < 2:
        return jsonify({"status": "waiting"})

    values = list(games[game_id].values())

    if None in values:
        return jsonify({"status": "waiting"})

    p1, p2 = values
    result = winner(p1, p2)

    return jsonify({
        "status": "done",
        "p1": p1,
        "p2": p2,
        "result": result
    })


@app.route("/")
def home():
    return "🔥 Two Player Game Server is Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
