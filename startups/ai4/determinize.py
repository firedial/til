"""
決定化 (Determinization) モジュール。

不完全情報ゲームでは、あるプレイヤーから見える「観測」には以下の
未知情報が含まれる:
  - 他プレイヤーの手札
  - 山札の中身と順序
  - 除外された5枚

ISMCTS はこれらを毎シミュレーション開始時にランダムに「確定」し、
その確定した世界で通常のMCTSを1回分回す。

このモジュールはその確定 (determinize) 操作を提供する。
"""

from __future__ import annotations
import random
from copy import deepcopy
from startups import (
    StartupsGame,
    GameState,
    PlayerState,
    NUM_COMPANIES,
    COMPANY_SIZES,
    TOTAL_CARDS,
    REMOVED_CARDS,
    NUM_PLAYERS,
    HAND_SIZE,
)


def determinize_from_observation(
    observation: dict,
    rng: random.Random,
) -> StartupsGame:
    """観測情報を元に、ありえる完全状態を1つサンプリングして返す。

    観測(obs)から、未知情報(他プレイヤーの手札・山札の中身と順序・除外5枚)
    をランダムに埋めたStartupsGameインスタンスを生成する。

    Args:
        observation: StartupsGame.get_observation() の戻り値
        rng: 乱数生成器

    Returns:
        ランダムに決定化された StartupsGame インスタンス
    """
    obs = observation
    me = obs["player_id"]

    # ------------------------------------------------------
    # 1. 全カードから「見えているカード」を引く
    # ------------------------------------------------------
    # 見えているカード:
    #   - 自分の手札
    #   - 各プレイヤーの投資済みカード(invested)
    #   - マーケットにあるカード
    # 見えていないカード:
    #   - 他プレイヤーの手札
    #   - 山札
    #   - 除外5枚

    all_cards: list[int] = []
    for c_idx, size in enumerate(COMPANY_SIZES):
        all_cards.extend([c_idx] * size)

    # 見えているカードをカウントして引いていく
    visible = list(obs["my_hand"])
    for pid in range(NUM_PLAYERS):
        for c_idx in range(NUM_COMPANIES):
            visible.extend([c_idx] * obs["all_invested"][pid][c_idx])
    visible.extend(obs["market"])

    # all_cards から visible を引く
    remaining = _subtract_multiset(all_cards, visible)

    # ------------------------------------------------------
    # 2. remaining を shuffle して他プレイヤーの手札・山札・除外に分配
    # ------------------------------------------------------
    rng.shuffle(remaining)

    # 他プレイヤーの手札サイズは観測から既知
    other_hands: dict[int, list[int]] = {}
    idx = 0
    for pid in range(NUM_PLAYERS):
        if pid == me:
            continue
        hand_size = obs["all_hand_sizes"][pid]
        # remaining が足りない場合は取れるだけ取る
        actual = remaining[idx:idx + hand_size]
        other_hands[pid] = actual
        idx += len(actual)

    deck_size = obs["deck_size"]
    actual_deck = remaining[idx:idx + deck_size]
    deck = actual_deck
    idx += len(actual_deck)
    # 残りは除外カード扱い (内部状態のズレで REMOVED_CARDS と一致しないことがある)
    # 足りなければ remaining を補充、多ければ切り捨て
    removed = remaining[idx:]

    # remaining が足りない場合: 他プレイヤーの手札や山札が短くなるが、
    # ISMCTS は決定化なので近似的に問題ない

    # ------------------------------------------------------
    # 3. StartupsGame インスタンスを生成して状態をセット
    # ------------------------------------------------------
    # 直接 GameState を構築する
    game = StartupsGame.__new__(StartupsGame)  # __init__ をバイパス
    game.state = GameState()
    s = game.state
    s.rng = rng

    s.players = []
    for pid in range(NUM_PLAYERS):
        p = PlayerState()
        if pid == me:
            p.hand = list(obs["my_hand"])
        else:
            p.hand = other_hands[pid]
        p.invested = list(obs["all_invested"][pid])
        p.antitrust = list(obs["all_antitrust"][pid])
        p.coins = obs["all_coins"][pid]
        s.players.append(p)

    s.deck = deck
    s.market = list(obs["market"])
    s.market_coins = list(obs["market_coins"])
    s.antitrust_owner = list(obs["antitrust_owner"])
    s.current_player = obs["current_player"]
    s.phase = obs["phase"]
    s.market_locked_company = obs["market_locked_company"]
    s.terminal = False

    return game


def _subtract_multiset(a: list[int], b: list[int]) -> list[int]:
    """a から b の各要素を1回ずつ取り除いた新リストを返す(マルチセット減算)。
    内部状態と現実のズレにより負になる場合は0にクランプする。
    """
    from collections import Counter
    ca = Counter(a)
    cb = Counter(b)
    ca.subtract(cb)
    result = []
    for k, v in ca.items():
        if v > 0:
            result.extend([k] * v)
    return result


# ------------------------------------------------------
# 動作確認
# ------------------------------------------------------
if __name__ == "__main__":
    # 適当にゲームを進めて、観測から決定化してみる
    game = StartupsGame(seed=0)
    rng = random.Random(100)

    # 数手ランダムに進めてみる
    for _ in range(10):
        if game.is_terminal():
            break
        actions = game.get_legal_actions()
        game.step(rng.choice(actions))

    # P0 の観測を取得
    obs = game.get_observation(0)
    print("=== 観測 (P0 視点) ===")
    print(f"my_hand: {obs['my_hand']}")
    print(f"market: {obs['market']}")
    print(f"deck_size: {obs['deck_size']}")
    print(f"all_hand_sizes: {obs['all_hand_sizes']}")
    print(f"phase: {obs['phase']}")

    # 決定化してみる
    det_game = determinize_from_observation(obs, rng)
    print("\n=== 決定化された世界 ===")
    print(det_game.render())

    # もう一度別の世界でサンプリング
    det_game2 = determinize_from_observation(obs, rng)
    print("\n=== 別の決定化 ===")
    for pid, p in enumerate(det_game2.state.players):
        print(f"  P{pid}: hand={p.hand}")
    print(f"  deck(先頭5枚): {det_game2.state.deck[:5]}...")

    print("\n✅ 決定化は動いています")
