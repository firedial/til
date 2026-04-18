"""
スタータップス Web UI — Flask バックエンド

エンドポイント:
  POST /api/setup      初期手札を受け取ってゲーム開始
  GET  /api/state      現在のゲーム状態を返す
  POST /api/human      人間の行動を適用
  POST /api/ai_draw    AIのドローを計算して返す (山札なら引いたカードを後で通知)
  POST /api/ai_reveal  AIが山札から引いたカードを通知 (めくった結果)
  POST /api/ai_play    AIのプレイを計算・適用して返す
  POST /api/reset      ゲームをリセット
"""

from flask import Flask, request, jsonify, send_from_directory
import os, random, torch
from startups import (
    StartupsGame, GameState, PlayerState,
    NUM_PLAYERS, NUM_COMPANIES, COMPANY_SIZES,
    INITIAL_COINS, REMOVED_CARDS,
)
from network import PolicyValueNet
from az_ismcts import AlphaZeroISMCTS

app = Flask(__name__, static_folder="web", static_url_path="")

COMPANY_LETTERS = ["A","B","C","D","E","F"]
AI_PLAYER = 2
AI_ITERATIONS = 100

# グローバル状態
game: StartupsGame = None
agent: AlphaZeroISMCTS = None
pending_ai_draw_action = None  # AIが山札を引く決定をした場合に保持


def load_model(path="az_net_trained.pt"):
    global agent
    net = PolicyValueNet(hidden=64, num_layers=2)
    net.load_state_dict(torch.load(path, weights_only=True))
    net.eval()
    agent = AlphaZeroISMCTS(net=net, iterations=AI_ITERATIONS, rng=random.Random(42))
    print(f"Model loaded: {path}")


def game_state_json():
    if game is None:
        return {"started": False}
    s = game.state
    players = []
    for i in range(NUM_PLAYERS):
        p = s.players[i]
        players.append({
            "id": i,
            "name": f"P{i}" if i != AI_PLAYER else "AI",
            "is_ai": i == AI_PLAYER,
            "coins": p.coins,
            "invested": list(p.invested),
            "antitrust": list(p.antitrust),
            "hand": [COMPANY_LETTERS[c] for c in p.hand] if i != AI_PLAYER else None,
            "hand_size": len(p.hand),
        })
    market = []
    for c, coins in zip(s.market, s.market_coins):
        market.append({"company": COMPANY_LETTERS[c], "coins": coins})

    result = {
        "started": True,
        "terminal": s.terminal,
        "current_player": s.current_player,
        "phase": s.phase,
        "deck_size": len(s.deck),
        "players": players,
        "market": market,
        "antitrust_owner": [
            (COMPANY_LETTERS[c] if s.antitrust_owner[c] >= 0 else None,
             s.antitrust_owner[c])
            for c in range(NUM_COMPANIES)
        ],
        "is_ai_turn": s.current_player == AI_PLAYER and not s.terminal,
    }
    if s.terminal:
        coins = [s.players[i].coins for i in range(NUM_PLAYERS)]
        w = game.get_winner()
        result["winner"] = w
        result["final_coins"] = coins
    return result


def legal_actions_json():
    actions = game.get_legal_actions()
    s = game.state
    pid = s.current_player
    p = s.players[pid]
    seen = {}
    result = []
    for a in actions:
        kind = a[0]
        if kind == "draw_deck":
            key = "draw_deck"
            if key not in seen:
                cost = 0
                if len(s.market) > 0:
                    has_free = any(p.antitrust[s.market[i]] == 1 for i in range(len(s.market)))
                    if not has_free:
                        cost = len(s.market)
                seen[key] = True
                result.append({"type": "draw_deck", "cost": cost, "action": list(a)})
        elif kind == "draw_market":
            c_idx = a[1]
            key = f"draw_market_{c_idx}"
            if key not in seen:
                coins_on = 0
                for j, mc in enumerate(s.market):
                    if mc == c_idx:
                        coins_on = s.market_coins[j]
                        break
                seen[key] = True
                result.append({"type": "draw_market", "company": COMPANY_LETTERS[c_idx],
                                "company_idx": c_idx, "coins_on": coins_on, "action": list(a)})
        elif kind in ("play_invest", "play_discard"):
            hand_idx = a[1]
            c_idx = p.hand[hand_idx]
            act_type = "invest" if kind == "play_invest" else "discard"
            key = f"{act_type}_{c_idx}"
            if key not in seen:
                seen[key] = True
                result.append({"type": act_type, "company": COMPANY_LETTERS[c_idx],
                                "company_idx": c_idx, "action": list(a)})
    return result


# ── Routes ──

@app.route("/")
def index():
    return send_from_directory("web", "index.html")


@app.route("/api/state")
def api_state():
    return jsonify(game_state_json())


@app.route("/api/setup", methods=["POST"])
def api_setup():
    global game, pending_ai_draw_action
    data = request.json
    hands_raw = data["hands"]  # [["A","B","E"], ["C","D","F"], ["A","E","F"]]
    hands = []
    for h in hands_raw:
        hands.append([COMPANY_INFO[c.upper()] for c in h])

    all_cards = []
    for c_idx, size in enumerate(COMPANY_SIZES):
        all_cards.extend([c_idx] * size)
    remaining = list(all_cards)
    for h in hands:
        for c in h:
            remaining.remove(c)
    rng = random.Random()
    rng.shuffle(remaining)
    deck_size = len(remaining) - REMOVED_CARDS

    game = StartupsGame.__new__(StartupsGame)
    game.state = GameState()
    s = game.state
    s.rng = rng
    s.deck = remaining[:deck_size]
    s.market = []
    s.market_coins = []
    s.players = []
    for pid in range(NUM_PLAYERS):
        p = PlayerState()
        p.hand = list(hands[pid])
        p.invested = [0] * NUM_COMPANIES
        p.coins = INITIAL_COINS
        p.antitrust = [0] * NUM_COMPANIES
        s.players.append(p)
    s.antitrust_owner = [-1] * NUM_COMPANIES
    s.current_player = 0
    s.phase = "draw"
    s.market_locked_company = None
    s.terminal = False
    pending_ai_draw_action = None
    return jsonify({"ok": True, **game_state_json()})


@app.route("/api/human", methods=["POST"])
def api_human():
    data = request.json
    action = tuple(data["action"])
    phase = game.state.phase

    if phase == "draw" and action[0] == "draw_deck":
        card_letter = data.get("drawn_card", "").upper()
        if card_letter in COMPANY_INFO:
            card = COMPANY_INFO[card_letter]
            s = game.state
            if card in s.deck:
                s.deck.remove(card)
            s.deck.insert(0, card)
    game.step(action)
    return jsonify({"ok": True, **game_state_json(), "legal": legal_actions_json() if not game.is_terminal() else []})


@app.route("/api/legal")
def api_legal():
    if game is None or game.is_terminal():
        return jsonify({"legal": []})
    return jsonify({"legal": legal_actions_json()})


@app.route("/api/ai_draw", methods=["POST"])
def api_ai_draw():
    global pending_ai_draw_action
    action = agent.search(game, root_player=AI_PLAYER)
    if action[0] == "draw_deck":
        pending_ai_draw_action = action
        s = game.state
        p = s.players[AI_PLAYER]
        cost = 0
        if len(s.market) > 0:
            has_free = any(p.antitrust[s.market[i]] == 1 for i in range(len(s.market)))
            if not has_free:
                cost = len(s.market)
        return jsonify({"draw_type": "deck", "cost": cost, "need_reveal": True})
    else:
        c_idx = action[1]
        game.step(action)
        pending_ai_draw_action = None
        return jsonify({"draw_type": "market", "company": COMPANY_LETTERS[c_idx],
                        "need_reveal": False, **game_state_json()})


@app.route("/api/ai_reveal", methods=["POST"])
def api_ai_reveal():
    global pending_ai_draw_action
    data = request.json
    card_letter = data["card"].upper()
    card = COMPANY_INFO[card_letter]
    s = game.state
    if card in s.deck:
        s.deck.remove(card)
    s.deck.insert(0, card)
    if pending_ai_draw_action:
        game.step(pending_ai_draw_action)
        pending_ai_draw_action = None
    return jsonify({"ok": True, **game_state_json()})


@app.route("/api/ai_play", methods=["POST"])
def api_ai_play():
    action = agent.search(game, root_player=AI_PLAYER)
    hand_idx = action[1]
    c_idx = game.state.players[AI_PLAYER].hand[hand_idx]
    act_type = "invest" if action[0] == "play_invest" else "discard"
    game.step(action)
    return jsonify({"type": act_type, "company": COMPANY_LETTERS[c_idx], **game_state_json()})


@app.route("/api/reset", methods=["POST"])
def api_reset():
    global game, pending_ai_draw_action
    game = None
    pending_ai_draw_action = None
    return jsonify({"ok": True})


COMPANY_INFO = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="az_net_trained.pt")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--ai-iterations", type=int, default=100)
    args = parser.parse_args()
    AI_ITERATIONS = args.ai_iterations
    load_model(args.model)
    os.makedirs("web", exist_ok=True)
    app.run(host="0.0.0.0", port=args.port, debug=False)
