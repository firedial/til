"""
スタータップス AI アシスタント (現物準拠モード)

現物のボードゲームを正として、ゲーム状態をこのツールに同期させる。
AI (P2) のターンだけ最善手を計算して表示する。

使い方:
    python play.py
    python play.py --model my_model.pt --ai-iterations 200

遊び方:
  1. 現物のルール通りにカードを配る
  2. 配られた初期手札を画面の指示に従って入力する
  3. 人間のターンは、現物で行ったアクションを入力する
  4. AIのターンは、画面に表示された行動を現物で実行する
"""

from __future__ import annotations
import argparse
import random
import sys
import torch
from startups import (
    StartupsGame, GameState, PlayerState,
    NUM_PLAYERS, NUM_COMPANIES, COMPANY_SIZES, TOTAL_CARDS,
    INITIAL_COINS, HAND_SIZE, REMOVED_CARDS,
)
from network import PolicyValueNet
from az_ismcts import AlphaZeroISMCTS

# 企業名
COMPANY_LETTERS = ["A", "B", "C", "D", "E", "F"]
COMPANY_INFO = {
    "A": (0, 5), "B": (1, 6), "C": (2, 7),
    "D": (3, 8), "E": (4, 9), "F": (5, 10),
}

AI_PLAYER = 2

# ANSIカラー
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"
    MAGENTA = "\033[95m"
    BG_GREEN = "\033[42m"
    BG_RED   = "\033[41m"
    BG_BLUE  = "\033[44m"

PLAYER_COLORS = [C.CYAN, C.YELLOW, C.MAGENTA]
PLAYER_NAMES  = ["P0 (人間)", "P1 (人間)", "P2 (AI)"]


# ============================================================
# 表示ヘルパー
# ============================================================

def fmt_hand(hand: list[int]) -> str:
    if not hand:
        return "(なし)"
    return " ".join(COMPANY_LETTERS[c] for c in sorted(hand))


def fmt_invested(inv: list[int]) -> str:
    parts = [f"{COMPANY_LETTERS[c]}x{n}" for c, n in enumerate(inv) if n > 0]
    return ", ".join(parts) if parts else "(なし)"


def fmt_antitrust(at: list[int]) -> str:
    owned = [COMPANY_LETTERS[c] for c, v in enumerate(at) if v == 1]
    return ", ".join(owned) if owned else "(なし)"


def fmt_market(market, coins):
    if not market:
        return "(空)"
    parts = []
    for c, co in zip(market, coins):
        s = COMPANY_LETTERS[c]
        if co > 0:
            s += f"(+{co}コイン)"
        parts.append(s)
    return "  ".join(parts)


def divider():
    print(f"{C.DIM}{'─' * 56}{C.RESET}")


def show_state(game: StartupsGame):
    s = game.state
    pid = s.current_player
    phase_jp = "ドロー" if s.phase == "draw" else "プレイ"

    print()
    divider()
    print(f"{C.BOLD}  山札: {len(s.deck)}枚  |  マーケット: {fmt_market(s.market, s.market_coins)}{C.RESET}")
    divider()
    for i in range(NUM_PLAYERS):
        p = s.players[i]
        color = PLAYER_COLORS[i]
        marker = f" {C.BG_GREEN}{C.BOLD} <- {phase_jp} {C.RESET}" if i == pid else ""
        print(f"  {color}{C.BOLD}{PLAYER_NAMES[i]}{C.RESET}{marker}")
        print(f"    コイン: {C.BOLD}{p.coins}{C.RESET}  |  投資: {fmt_invested(p.invested)}")
        at_str = fmt_antitrust(p.antitrust)
        hand_str = f"{len(p.hand)}枚" if i == AI_PLAYER else fmt_hand(p.hand)
        print(f"    独禁: {at_str}  |  手札: {hand_str}")
    divider()


# ============================================================
# 入力ヘルパー
# ============================================================

def input_line(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print(f"\n{C.RED}中断しました{C.RESET}")
        sys.exit(0)


def input_int(prompt: str, lo: int, hi: int) -> int:
    while True:
        raw = input_line(prompt)
        try:
            v = int(raw)
            if lo <= v <= hi:
                return v
        except ValueError:
            pass
        print(f"  {C.RED}{lo}~{hi} の数字を入力してください{C.RESET}")


def input_company(prompt: str) -> int:
    while True:
        raw = input_line(prompt).upper()
        if raw in COMPANY_INFO:
            return COMPANY_INFO[raw][0]
        print(f"  {C.RED}A~F のいずれかを入力してください{C.RESET}")


def input_companies(prompt: str, count: int) -> list[int]:
    while True:
        raw = input_line(prompt).upper().split()
        if len(raw) != count:
            print(f"  {C.RED}{count}枚分の企業名をスペース区切りで入力 (例: A B E){C.RESET}")
            continue
        valid = True
        result = []
        for r in raw:
            if r in COMPANY_INFO:
                result.append(COMPANY_INFO[r][0])
            else:
                print(f"  {C.RED}'{r}' は無効です。A~F を入力してください{C.RESET}")
                valid = False
                break
        if valid:
            return result


# ============================================================
# 初期セットアップ (現物に合わせる)
# ============================================================

def setup_game_from_physical() -> StartupsGame:
    print(f"\n{C.BOLD}  初期手札を入力してください{C.RESET}")
    print(f"{C.DIM}  現物で配られた3枚を、企業名 (A-F) で入力します{C.RESET}")
    print(f"{C.DIM}  企業: A(5枚) B(6枚) C(7枚) D(8枚) E(9枚) F(10枚){C.RESET}\n")

    hands = []
    for pid in range(NUM_PLAYERS):
        color = PLAYER_COLORS[pid]
        h = input_companies(
            f"  {color}{PLAYER_NAMES[pid]} の手札 (3枚): {C.RESET}", 3
        )
        hands.append(h)
        print(f"    -> {fmt_hand(h)}")

    # 残りカードから山札を作る
    all_cards = []
    for c_idx, size in enumerate(COMPANY_SIZES):
        all_cards.extend([c_idx] * size)

    remaining = list(all_cards)
    for h in hands:
        for c in h:
            remaining.remove(c)

    # remaining = 除外5枚 + 山札
    # 現物ではどの5枚が除外されたか不明
    # → ランダムにシャッフルして山札とする (AI推論時は決定化で上書き)
    rng = random.Random()
    rng.shuffle(remaining)
    deck_size = len(remaining) - REMOVED_CARDS

    # ゲーム状態を手動構築
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

    print(f"\n  {C.GREEN}セットアップ完了! 山札: {deck_size}枚{C.RESET}")
    return game


# ============================================================
# 人間ターンの入力
# ============================================================

def input_human_draw(game: StartupsGame):
    s = game.state
    pid = s.current_player
    p = s.players[pid]
    color = PLAYER_COLORS[pid]
    actions = game.get_legal_actions()

    can_draw_deck = any(a[0] == "draw_deck" for a in actions)
    market_companies = sorted(set(
        a[1] for a in actions if a[0] == "draw_market"
    ))

    print(f"\n  {color}{C.BOLD}{PLAYER_NAMES[pid]} のドロー:{C.RESET}")
    options = []
    if can_draw_deck:
        cost = 0
        if len(s.market) > 0:
            has_free = any(p.antitrust[s.market[i]] == 1 for i in range(len(s.market)))
            if not has_free:
                cost = len(s.market)
        cost_str = f" (コイン{cost}枚支払い)" if cost > 0 else ""
        options.append(("deck", -1))
        print(f"    {C.GREEN}1{C.RESET}) 山札から引く{cost_str}")

    for c_idx in market_companies:
        coins_on = 0
        for j, mc in enumerate(s.market):
            if mc == c_idx:
                coins_on = s.market_coins[j]
                break
        coin_str = f" (+{coins_on}コイン)" if coins_on > 0 else ""
        n = len(options) + 1
        options.append(("market", c_idx))
        print(f"    {C.GREEN}{n}{C.RESET}) マーケットから {COMPANY_LETTERS[c_idx]} を取る{coin_str}")

    choice = input_int(f"\n  {color}番号: {C.RESET}", 1, len(options)) - 1

    if options[choice][0] == "deck":
        card = input_company(f"  {C.DIM}引いたカードの企業名: {C.RESET}")
        # 山札操作: そのカードを先頭に
        if card in s.deck:
            s.deck.remove(card)
        s.deck.insert(0, card)
        game.step(("draw_deck",))
        print(f"  -> {COMPANY_LETTERS[card]} を引きました")
    else:
        c_idx = options[choice][1]
        game.step(("draw_market", c_idx))
        print(f"  -> マーケットから {COMPANY_LETTERS[c_idx]} を取りました")


def input_human_play(game: StartupsGame):
    s = game.state
    pid = s.current_player
    p = s.players[pid]
    color = PLAYER_COLORS[pid]
    actions = game.get_legal_actions()

    print(f"\n  {color}{C.BOLD}{PLAYER_NAMES[pid]} のプレイ:{C.RESET}")
    print(f"  {C.DIM}手札: {fmt_hand(p.hand)}{C.RESET}")

    # 投資/放流を企業名ベースで表示 (重複除去)
    invest_set = set()
    discard_set = set()
    action_lookup = {}
    for a in actions:
        hand_idx = a[1]
        c_idx = p.hand[hand_idx]
        if a[0] == "play_invest" and c_idx not in invest_set:
            invest_set.add(c_idx)
            action_lookup[("invest", c_idx)] = a
        elif a[0] == "play_discard" and c_idx not in discard_set:
            discard_set.add(c_idx)
            action_lookup[("discard", c_idx)] = a

    options = []
    for c_idx in sorted(invest_set):
        n = len(options) + 1
        options.append(("invest", c_idx))
        print(f"    {C.GREEN}{n}{C.RESET}) {COMPANY_LETTERS[c_idx]} に投資")
    for c_idx in sorted(discard_set):
        n = len(options) + 1
        options.append(("discard", c_idx))
        print(f"    {C.GREEN}{n}{C.RESET}) {COMPANY_LETTERS[c_idx]} をマーケットに放流")

    choice = input_int(f"\n  {color}番号: {C.RESET}", 1, len(options)) - 1
    kind, c_idx = options[choice]
    game.step(action_lookup[(kind, c_idx)])
    if kind == "invest":
        print(f"  -> {COMPANY_LETTERS[c_idx]} に投資しました")
    else:
        print(f"  -> {COMPANY_LETTERS[c_idx]} を放流しました")


# ============================================================
# AIターン
# ============================================================

def ai_turn(game: StartupsGame, agent: AlphaZeroISMCTS):
    color = PLAYER_COLORS[AI_PLAYER]
    s = game.state

    # --- ドロー ---
    print(f"\n  {color}{C.BOLD}  AI が考え中...{C.RESET}", end="", flush=True)
    action = agent.search(game, root_player=AI_PLAYER)

    if action[0] == "draw_deck":
        p = s.players[AI_PLAYER]
        cost = 0
        if len(s.market) > 0:
            has_free = any(p.antitrust[s.market[i]] == 1 for i in range(len(s.market)))
            if not has_free:
                cost = len(s.market)
        cost_str = f" (コイン{cost}枚支払い)" if cost > 0 else ""
        print(f"\r  {color}{C.BOLD}  AI のドロー: 山札から引く{cost_str}{C.RESET}          ")
        print(f"  {C.DIM}-> 現物の山札をめくって AI の手札に伏せてください{C.RESET}")
        card = input_company(f"  {C.DIM}めくったカードの企業名: {C.RESET}")
        if card in s.deck:
            s.deck.remove(card)
        s.deck.insert(0, card)
        game.step(action)

    elif action[0] == "draw_market":
        c_idx = action[1]
        print(f"\r  {color}{C.BOLD}  AI のドロー: マーケットから {COMPANY_LETTERS[c_idx]} を取る{C.RESET}          ")
        print(f"  {C.DIM}-> マーケットの {COMPANY_LETTERS[c_idx]} を AI の手札に移してください{C.RESET}")
        game.step(action)

    # --- プレイ ---
    show_state(game)
    print(f"\n  {color}{C.BOLD}  AI が考え中...{C.RESET}", end="", flush=True)
    action = agent.search(game, root_player=AI_PLAYER)
    hand_idx = action[1]
    c_idx = game.state.players[AI_PLAYER].hand[hand_idx]

    if action[0] == "play_invest":
        print(f"\r  {color}{C.BOLD}  AI のプレイ: {COMPANY_LETTERS[c_idx]} に投資{C.RESET}                  ")
        print(f"  {C.DIM}-> AI の手札から {COMPANY_LETTERS[c_idx]} を投資エリアに出してください{C.RESET}")
    elif action[0] == "play_discard":
        print(f"\r  {color}{C.BOLD}  AI のプレイ: {COMPANY_LETTERS[c_idx]} をマーケットに放流{C.RESET}                  ")
        print(f"  {C.DIM}-> AI の手札から {COMPANY_LETTERS[c_idx]} をマーケットに出してください{C.RESET}")

    game.step(action)
    input(f"  {C.DIM}(現物を操作したら Enter){C.RESET}")


# ============================================================
# 結果表示
# ============================================================

def show_result(game: StartupsGame):
    s = game.state
    print()
    print(f"{C.BOLD}{'=' * 56}{C.RESET}")
    print(f"{C.BOLD}  ゲーム終了!{C.RESET}")
    print(f"{'=' * 56}")
    for i in range(NUM_PLAYERS):
        p = s.players[i]
        color = PLAYER_COLORS[i]
        print(f"\n  {color}{C.BOLD}{PLAYER_NAMES[i]}{C.RESET}")
        print(f"    投資: {fmt_invested(p.invested)}")
        print(f"    最終コイン: {C.BOLD}{p.coins}{C.RESET}")

    print()
    divider()
    w = game.get_winner()
    if w is not None:
        coins = s.players[w].coins
        if w == AI_PLAYER:
            print(f"  {C.BG_RED}{C.BOLD}  AI の勝利! ({coins}コイン) {C.RESET}")
        else:
            name = PLAYER_NAMES[w].split(" (")[0]
            print(f"  {C.BG_GREEN}{C.BOLD}  {name} の勝利! ({coins}コイン) {C.RESET}")
    else:
        print(f"  {C.BOLD}引き分け!{C.RESET}")
    divider()

    print(f"\n  {C.DIM}[企業ごとの内訳]{C.RESET}")
    for c in range(NUM_COMPANIES):
        counts = [s.players[i].invested[c] for i in range(NUM_PLAYERS)]
        if max(counts) == 0:
            continue
        top_count = max(counts)
        tops = [i for i, v in enumerate(counts) if v == top_count]
        if len(tops) == 1:
            status = f"-> {PLAYER_NAMES[tops[0]].split(' (')[0]} が独占"
        else:
            status = "-> 同数 (徴収なし)"
        cards = "  ".join(f"P{i}:{v}" for i, v in enumerate(counts) if v > 0)
        print(f"    {COMPANY_LETTERS[c]}: {cards}  {status}")


# ============================================================
# メイン
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="スタータップス AI アシスタント")
    parser.add_argument("--model", default="az_net_trained.pt", help="学習済みモデル")
    parser.add_argument("--ai-iterations", type=int, default=100, help="AI思考回数")
    args = parser.parse_args()

    print(f"\n{C.BOLD}  スタータップス AI アシスタント{C.RESET}")
    print(f"{C.DIM}  現物のボードゲームに AI を1人参加させます{C.RESET}")
    print(f"{C.DIM}  P0, P1 = 人間  |  P2 = AI{C.RESET}")
    print(f"{C.DIM}  企業: A(5枚) B(6枚) C(7枚) D(8枚) E(9枚) F(10枚){C.RESET}")

    try:
        net = PolicyValueNet(hidden=64, num_layers=2)
        net.load_state_dict(torch.load(args.model, weights_only=True))
        net.eval()
        print(f"\n  {C.GREEN}AI モデル読み込み完了{C.RESET}")
    except FileNotFoundError:
        print(f"\n  {C.RED}{args.model} が見つかりません{C.RESET}")
        print(f"  {C.DIM}先に python train_and_evaluate.py で学習してください{C.RESET}")
        sys.exit(1)

    agent = AlphaZeroISMCTS(
        net=net, iterations=args.ai_iterations, rng=random.Random(42)
    )

    game = setup_game_from_physical()
    input(f"\n  {C.DIM}Enter でゲーム開始...{C.RESET}")

    while not game.is_terminal():
        show_state(game)
        pid = game.current_player()

        if pid == AI_PLAYER:
            ai_turn(game, agent)
        else:
            if game.state.phase == "draw":
                input_human_draw(game)
                show_state(game)
                input_human_play(game)
            else:
                input_human_play(game)

    show_result(game)


if __name__ == "__main__":
    main()
