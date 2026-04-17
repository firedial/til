"""
状態と行動を NN 用にエンコードする。

方針:
  - 状態: 観測を固定長ベクトルに (float32)
  - 行動: 固定長の行動空間にマッピング
    行動空間 (size = ACTION_SIZE):
      0       : draw_deck
      1..6    : draw_market(company_idx)    (6種)
      7..12   : play_invest  (company 0..5) (6種)
      13..18  : play_discard (company 0..5) (6種)
    合計 1 + 6 + 6 + 6 = 19

注意:
  - play_invest/play_discard は「手札の位置」ではなく「会社ID」で表現
    合法手の中に同じ (kind, company) の重複があれば最初のインスタンスを使う
"""

from __future__ import annotations
import numpy as np
from startups import NUM_COMPANIES, NUM_PLAYERS


# ============================================================
# 行動空間
# ============================================================

ACTION_SIZE = 1 + NUM_COMPANIES + NUM_COMPANIES + NUM_COMPANIES  # 19

# 行動インデックス変換
def action_to_index(action: tuple) -> int:
    """内部行動 (tuple) を action space の index に変換。"""
    kind = action[0]
    if kind == "draw_deck":
        return 0
    elif kind == "draw_market":
        return 1 + action[1]
    elif kind == "play_invest":
        # action は ("play_invest", hand_idx) だが、hand_idx から company を引き当てる必要がある
        # → このヘルパーだけではダメ。代わりに外部から company を渡すラッパーを使う。
        raise ValueError("Use action_to_index_with_game() for play actions")
    elif kind == "play_discard":
        raise ValueError("Use action_to_index_with_game() for play actions")
    else:
        raise ValueError(f"Unknown action kind: {kind}")


def action_to_index_with_game(action: tuple, game) -> int:
    """ゲーム状態を使って、手札位置から会社IDに変換したうえでインデックス化。"""
    kind = action[0]
    if kind == "draw_deck":
        return 0
    elif kind == "draw_market":
        return 1 + action[1]
    elif kind in ("play_invest", "play_discard"):
        hand_idx = action[1]
        pid = game.current_player()
        c_idx = game.state.players[pid].hand[hand_idx]
        base = 7 if kind == "play_invest" else 13
        return base + c_idx
    else:
        raise ValueError(f"Unknown action kind: {kind}")


def get_legal_action_mask(game) -> np.ndarray:
    """合法な action index だけ 1、それ以外は 0 の配列を返す。"""
    mask = np.zeros(ACTION_SIZE, dtype=np.float32)
    for a in game.get_legal_actions():
        idx = action_to_index_with_game(a, game)
        mask[idx] = 1.0
    return mask


def get_legal_action_map(game) -> dict[int, tuple]:
    """action index → 内部行動(tuple) のマッピングを返す。

    同じインデックスに複数の内部行動(手札位置違いで同じ会社IDなど)が
    対応する場合、最初のものを使う。これは意味論的に同じ行動なので問題ない。
    """
    m: dict[int, tuple] = {}
    for a in game.get_legal_actions():
        idx = action_to_index_with_game(a, game)
        if idx not in m:
            m[idx] = a
    return m


# ============================================================
# 状態エンコーディング
# ============================================================

def encode_observation(obs: dict) -> np.ndarray:
    """観測を固定長ベクトルに変換。

    構成 (全 67 次元):
      [0..5]    自分の手札 (会社ごとの枚数)
      [6]       自分のコイン (/20 でスケール)
      [7..12]   自分の投資
      [13..18]  自分の独禁チップ
      [19..24]  相手1の投資
      [25..30]  相手1の独禁チップ
      [31]      相手1のコイン (/20)
      [32]      相手1の手札枚数 (/10)
      [33..38]  相手2の投資
      [39..44]  相手2の独禁チップ
      [45]      相手2のコイン (/20)
      [46]      相手2の手札枚数 (/10)
      [47..52]  マーケットのカード構成
      [53]      マーケット上のコイン合計 (/10)
      [54]      山札残枚数 (/30)
      [55, 56]  フェーズ (draw, play の one-hot)
      [57..62]  market_locked_company (会社ごとの one-hot、なしなら全0)
      [63..65]  current_player の one-hot (3人ぶん)
      [66]      自分が current_player か (0/1)
    """
    me = obs["player_id"]

    # 手札を会社ごとの枚数にまとめる
    hand_counts = [0] * NUM_COMPANIES
    for c_idx in obs["my_hand"]:
        hand_counts[c_idx] += 1

    # マーケットも会社ごとの枚数に
    market_counts = [0] * NUM_COMPANIES
    for c_idx in obs["market"]:
        market_counts[c_idx] += 1

    # 相手2人の情報を並べる (自分を除く)
    others = [p for p in range(NUM_PLAYERS) if p != me]

    feats = []
    feats.extend(hand_counts)                              # [0..5]
    feats.append(obs["my_coins"] / 20.0)                   # [6]
    feats.extend(obs["my_invested"])                       # [7..12]
    feats.extend(obs["my_antitrust"])                      # [13..18]
    for op in others:
        feats.extend(obs["all_invested"][op])              # [19..24], [33..38]
        feats.extend(obs["all_antitrust"][op])             # [25..30], [39..44]
        feats.append(obs["all_coins"][op] / 20.0)          # [31], [45]
        feats.append(obs["all_hand_sizes"][op] / 10.0)     # [32], [46]
    feats.extend(market_counts)                            # [47..52]
    feats.append(sum(obs["market_coins"]) / 10.0)          # [53]
    feats.append(obs["deck_size"] / 30.0)                  # [54]
    # フェーズ one-hot
    feats.append(1.0 if obs["phase"] == "draw" else 0.0)   # [55]
    feats.append(1.0 if obs["phase"] == "play" else 0.0)   # [56]
    # market_locked_company one-hot
    locked = obs["market_locked_company"]
    locked_onehot = [0.0] * NUM_COMPANIES
    if locked is not None:
        locked_onehot[locked] = 1.0
    feats.extend(locked_onehot)                            # [57..62]
    # current_player one-hot
    cp_onehot = [0.0] * NUM_PLAYERS
    cp_onehot[obs["current_player"]] = 1.0
    feats.extend(cp_onehot)                                # [63..65]
    # 自分のターンか
    feats.append(1.0 if obs["current_player"] == me else 0.0)  # [66]

    arr = np.array(feats, dtype=np.float32)
    assert arr.shape == (OBSERVATION_SIZE,), f"Shape mismatch: {arr.shape}"
    return arr


OBSERVATION_SIZE = 67


# ============================================================
# 動作確認
# ============================================================

if __name__ == "__main__":
    from startups import StartupsGame
    import random

    game = StartupsGame(seed=42)
    rng = random.Random(1)

    # 数手進めてみる
    for _ in range(5):
        if game.is_terminal():
            break
        actions = game.get_legal_actions()
        game.step(rng.choice(actions))

    obs = game.get_observation(0)
    vec = encode_observation(obs)
    print(f"観測ベクトル shape: {vec.shape}")
    print(f"値: {vec}")
    print(f"\n観測の具体情報:")
    print(f"  手札: {obs['my_hand']}  → エンコード済 手札枚数 {vec[:6]}")
    print(f"  自分コイン: {obs['my_coins']}  → エンコード値 {vec[6]:.3f} (正規化済)")
    print(f"  フェーズ: {obs['phase']}")

    mask = get_legal_action_mask(game)
    print(f"\n合法手マスク: {mask}")
    print(f"合法手数: {int(mask.sum())}")

    action_map = get_legal_action_map(game)
    print(f"\n合法手マップ:")
    for idx, a in action_map.items():
        print(f"  index {idx} → {a}")
