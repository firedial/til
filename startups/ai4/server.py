"""
スタータップス Web UI — Flask バックエンド
3モード: battle(対戦) / real(リアル) / debug(デバッグ)
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
from encoding import action_to_index_with_game

app = Flask(__name__, static_folder="web", static_url_path="")

COMPANY_NUMS = [5, 6, 7, 8, 9, 10]  # 企業名 = 数字
NUM_TO_IDX = {5:0, 6:1, 7:2, 8:3, 9:4, 10:5}
IDX_TO_NUM = {i:n for n,i in NUM_TO_IDX.items()}
AI_PLAYER_BATTLE = [1, 2]  # battle モードでのAI担当
AI_PLAYER_DEBUG = 2
AI_ITERATIONS = 100

game: StartupsGame = None
agent: AlphaZeroISMCTS = None
pending_ai_draw = None
mode = "battle"  # "battle" | "real" | "debug"
real_player = 0  # real モードで情報を見るプレイヤー
human_player = 0  # battle モードでの人間の席番号
history = []  # undo 用: GameState の deepcopy リスト


def load_model(path="az_net_trained.pt", hidden=64, layers=2):
    global agent
    net = PolicyValueNet(hidden=hidden, num_layers=layers)
    net.load_state_dict(torch.load(path, weights_only=True))
    net.eval()
    agent = AlphaZeroISMCTS(net=net, iterations=AI_ITERATIONS, rng=random.Random(42))


def save_snapshot():
    """現在のゲーム状態を history に保存 (undo 用)。"""
    from copy import deepcopy
    if game is not None:
        history.append(deepcopy(game.state))


def _draw_cost(player, market):
    return sum(1 for c in market if player.antitrust[c] == 0)


def _c(idx):
    """企業indexを数字に変換"""
    return COMPANY_NUMS[idx]


def game_state_json(for_player=None):
    """ゲーム状態JSON。for_player指定時はその視点のみ(リアルモード用)。"""
    if game is None:
        return {"started": False}
    s = game.state
    players = []
    for i in range(NUM_PLAYERS):
        p = s.players[i]
        show_hand = True
        if for_player is not None and i != for_player:
            show_hand = False
        if mode == "debug":
            show_hand = True

        pdata = {
            "id": i,
            "coins": p.coins,
            "invested": list(p.invested),
            "antitrust": list(p.antitrust),
            "hand": [_c(c) for c in p.hand] if show_hand else None,
            "hand_size": len(p.hand),
        }
        players.append(pdata)

    market = []
    for idx, (c, coins) in enumerate(zip(s.market, s.market_coins)):
        market.append({"company": _c(c), "company_idx": c, "coins": coins, "market_pos": idx})

    result = {
        "started": True, "terminal": s.terminal,
        "current_player": s.current_player, "phase": s.phase,
        "deck_size": len(s.deck), "players": players, "market": market,
        "mode": mode, "human_player": human_player,
    }
    if s.terminal:
        result["winner"] = game.get_winner()
        result["final_coins"] = [s.players[i].coins for i in range(NUM_PLAYERS)]
        result["ranking"] = game.get_ranking()
        result["rewards"] = game.get_rewards()
    return result


def legal_actions_list(include_market_pos=False):
    """合法手リスト。include_market_pos=Trueならマーケット位置(コイン違い)で分離。"""
    actions = game.get_legal_actions()
    s = game.state
    pid = s.current_player
    p = s.players[pid]
    result = []

    if s.phase == "draw":
        # draw_deck
        has_draw_deck = any(a[0] == "draw_deck" for a in actions)
        if has_draw_deck:
            cost = _draw_cost(p, s.market)
            result.append({"type": "draw_deck", "cost": cost, "action": ["draw_deck"]})

        # draw_market: コイン別に分離
        if include_market_pos:
            seen_positions = set()
            for a in actions:
                if a[0] == "draw_market":
                    c_idx = a[1]
                    # 同企業で複数枚ある場合、コインが違うカードを別選択肢に
                    for mi, mc in enumerate(s.market):
                        if mc == c_idx and mi not in seen_positions:
                            seen_positions.add(mi)
                            coins_on = s.market_coins[mi]
                            result.append({
                                "type": "draw_market",
                                "company": _c(c_idx), "company_idx": c_idx,
                                "coins_on": coins_on, "market_pos": mi,
                                "action": ["draw_market", c_idx],
                            })
        else:
            seen = set()
            for a in actions:
                if a[0] == "draw_market":
                    c_idx = a[1]
                    if c_idx not in seen:
                        seen.add(c_idx)
                        coins_on = 0
                        for j, mc in enumerate(s.market):
                            if mc == c_idx:
                                coins_on = s.market_coins[j]
                                break
                        result.append({
                            "type": "draw_market",
                            "company": _c(c_idx), "company_idx": c_idx,
                            "coins_on": coins_on,
                            "action": ["draw_market", c_idx],
                        })

    elif s.phase == "play":
        seen = {}
        for a in actions:
            hand_idx = a[1]
            c_idx = p.hand[hand_idx]
            act_type = "invest" if a[0] == "play_invest" else "discard"
            key = f"{act_type}_{c_idx}"
            if key not in seen:
                seen[key] = True
                result.append({
                    "type": act_type, "company": _c(c_idx), "company_idx": c_idx,
                    "action": list(a),
                })
    return result


# ── Routes ──

@app.route("/")
def index():
    return send_from_directory("web", "index.html")

@app.route("/api/state")
def api_state():
    fp = real_player if mode == "real" else None
    return jsonify(game_state_json(for_player=fp))

@app.route("/api/setup", methods=["POST"])
def api_setup():
    global game, pending_ai_draw, mode, real_player, human_player
    data = request.json
    mode = data.get("mode", "battle")
    real_player = data.get("real_player", 0)
    human_player = real_player
    hands_raw = data["hands"]  # [[5,6,10], [7,8,9], [5,9,10]] 数字で来る
    hands = [[NUM_TO_IDX[int(c)] for c in h] for h in hands_raw]

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
    s.market, s.market_coins = [], []
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
    s.turn_order = list(range(NUM_PLAYERS))
    s.terminal = False
    pending_ai_draw = None

    fp = real_player if mode == "real" else None
    return jsonify({"ok": True, **game_state_json(for_player=fp)})

@app.route("/api/auto_setup", methods=["POST"])
def api_auto_setup():
    """対戦モード用: 全自動でカードを配る。人間の席はランダム。"""
    global game, pending_ai_draw, mode, real_player, human_player
    data = request.json or {}
    mode = data.get("mode", "battle")

    game = StartupsGame(seed=random.randint(0, 10**9))
    pending_ai_draw = None
    human_player = random.randint(0, NUM_PLAYERS - 1)
    real_player = human_player

    fp = human_player if mode == "battle" else None
    result = game_state_json(for_player=fp)
    result["human_player"] = human_player
    return jsonify({"ok": True, **result})

@app.route("/api/legal")
def api_legal():
    if game is None or game.is_terminal():
        return jsonify({"legal": []})
    return jsonify({"legal": legal_actions_list(include_market_pos=True)})

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """全選択肢の順位ポイント期待値を計算。"""
    if game is None or game.is_terminal():
        return jsonify({"actions": []})
    pid = game.current_player()
    _, stats = agent.search(game, root_player=pid, return_stats=True)
    legal = legal_actions_list(include_market_pos=True)

    for item in legal:
        action_tuple = tuple(item["action"])
        try:
            idx = action_to_index_with_game(action_tuple, game)
        except Exception:
            idx = -1
        if idx in stats:
            item["ep"] = stats[idx]["expected_points"]
            item["visits"] = stats[idx]["visits"]
        else:
            item["ep"] = 0.5
            item["visits"] = 0

    if legal:
        best_ep = max(a["ep"] for a in legal)
        for a in legal:
            a["is_best"] = abs(a["ep"] - best_ep) < 0.001
    return jsonify({"actions": legal, "player": pid})

@app.route("/api/human", methods=["POST"])
def api_human():
    data = request.json
    action = tuple(data["action"])
    save_snapshot()
    if game.state.phase == "draw" and action[0] == "draw_deck":
        card_num = data.get("drawn_card")
        if card_num is not None:
            card = NUM_TO_IDX[int(card_num)]
            s = game.state
            if card in s.deck:
                s.deck.remove(card)
            s.deck.insert(0, card)
    game.step(action)
    fp = human_player if mode == "battle" else (real_player if mode == "real" else None)
    return jsonify({"ok": True, **game_state_json(for_player=fp)})

@app.route("/api/other_action", methods=["POST"])
def api_other_action():
    """行動を企業番号ベースで受け付ける。

    自分(real_player)の場合は手札チェックあり。
    他プレイヤーの場合は手札が見えないので、手札になくても強制的に処理する。

    リクエスト例:
      ドロー: {"type": "draw_deck"}
      マーケット取得: {"type": "draw_market", "company": 7}
      投資: {"type": "invest", "company": 8}
      放流: {"type": "discard", "company": 6}
    """
    data = request.json
    s = game.state
    pid = s.current_player
    p = s.players[pid]
    act_type = data["type"]
    is_self = (pid == real_player)

    save_snapshot()

    if s.phase == "draw":
        if act_type == "draw_deck":
            game.step(("draw_deck",))
        elif act_type == "draw_market":
            c_idx = NUM_TO_IDX[int(data["company"])]
            game.step(("draw_market", c_idx))
        else:
            history.pop()  # snapshot を戻す
            return jsonify({"error": f"Invalid draw action: {act_type}"}), 400

    elif s.phase == "play":
        c_idx = NUM_TO_IDX[int(data["company"])]
        # 手札からその企業のカードを見つける
        hand_idx = None
        for i, hc in enumerate(p.hand):
            if hc == c_idx:
                hand_idx = i
                break

        if hand_idx is None:
            if is_self:
                # 自分の手札にない → エラー
                history.pop()
                return jsonify({"error": f"手札に {data['company']} がありません"}), 400
            else:
                # 他プレイヤー → 手札が内部状態と現実でズレている
                # 手札の中の1枚を正しい企業に差し替えて処理する
                # (山札から引いたカードが内部と現実で異なるため)
                if len(p.hand) > 0:
                    # 末尾のカードを差し替え (直近に山札から引いたカードのはず)
                    p.hand[-1] = c_idx
                    hand_idx = len(p.hand) - 1
                else:
                    # 手札が空 (通常ありえないが安全策)
                    history.pop()
                    return jsonify({"error": "手札が空です"}), 400

        if act_type == "invest":
            game.step(("play_invest", hand_idx))
        elif act_type == "discard":
            game.step(("play_discard", hand_idx))
        else:
            history.pop()
            return jsonify({"error": f"Invalid play action: {act_type}"}), 400

    fp = real_player if mode == "real" else None
    return jsonify({"ok": True, **game_state_json(for_player=fp)})

@app.route("/api/ai_turn", methods=["POST"])
def api_ai_turn():
    """AI のドロー+プレイを一括実行。drawn_card が必要なら need_reveal を返す。"""
    global pending_ai_draw
    data = request.get_json(silent=True) or {}
    pid = game.current_player()

    save_snapshot()

    if game.state.phase == "draw":
        if pending_ai_draw is not None:
            # reveal が来た
            card_num = data.get("drawn_card")
            if card_num is not None:
                card = NUM_TO_IDX[int(card_num)]
                s = game.state
                if card in s.deck:
                    s.deck.remove(card)
                s.deck.insert(0, card)
            game.step(pending_ai_draw)
            pending_ai_draw = None
        else:
            action = agent.search(game, root_player=pid)
            if action[0] == "draw_deck":
                if mode == "battle":
                    # 対戦モード: 山札ドローも自動 (カード入力不要)
                    drawn_card = _c(game.state.deck[0])  # 引くカードの数字
                    game.step(action)
                    fp = human_player if mode == "battle" else (real_player if mode == "real" else None)
                    return jsonify({"phase": "draw", "draw_type": "deck", "drawn_card": drawn_card,
                                    "need_reveal": False, **game_state_json(for_player=fp)})
                else:
                    # リアル/デバッグ: めくったカードの入力が必要
                    pending_ai_draw = action
                    cost = _draw_cost(game.state.players[pid], game.state.market)
                    return jsonify({"phase": "draw", "draw_type": "deck", "cost": cost, "need_reveal": True})
            else:
                c_idx = action[1]
                game.step(action)
                fp = real_player if mode == "real" else None
                return jsonify({"phase": "draw", "draw_type": "market", "company": _c(c_idx),
                                "need_reveal": False, **game_state_json(for_player=fp)})

    # play phase
    if game.state.phase == "play":
        action = agent.search(game, root_player=pid)
        hand_idx = action[1]
        c_idx = game.state.players[pid].hand[hand_idx]
        act_type = "invest" if action[0] == "play_invest" else "discard"
        game.step(action)
        fp = real_player if mode == "real" else None
        return jsonify({"phase": "play", "type": act_type, "company": _c(c_idx),
                        **game_state_json(for_player=fp)})

    fp = real_player if mode == "real" else None
    return jsonify(game_state_json(for_player=fp))

@app.route("/api/undo", methods=["POST"])
def api_undo():
    """直前の行動を取り消す。"""
    global pending_ai_draw
    if not history:
        return jsonify({"error": "これ以上戻せません"}), 400
    game.state = history.pop()
    pending_ai_draw = None
    fp = real_player if mode == "real" else (human_player if mode == "battle" else None)
    return jsonify({"ok": True, "undo_remaining": len(history), **game_state_json(for_player=fp)})

@app.route("/api/reset", methods=["POST"])
def api_reset():
    global game, pending_ai_draw, history
    game = None
    pending_ai_draw = None
    history = []
    return jsonify({"ok": True})

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="az_net_trained.pt")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--ai-iterations", type=int, default=100)
    parser.add_argument("--hidden", type=int, default=64)
    parser.add_argument("--layers", type=int, default=2)
    args = parser.parse_args()
    AI_ITERATIONS = args.ai_iterations
    load_model(args.model, args.hidden, args.layers)
    os.makedirs("web", exist_ok=True)
    app.run(host="0.0.0.0", port=args.port, debug=False)
