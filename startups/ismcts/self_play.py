"""
自己対戦でトレーニングデータを収集。

1ゲーム = 複数の学習サンプルを生成:
    (state_vector, policy_target, value_target, legal_mask)

- state_vector: その手番の観測ベクトル
- policy_target: その局面でのMCTS訪問分布 (≈ 「正解の方策」)
- value_target: 最終的に root_player が勝ったか (-1, 0, 1)
- legal_mask: 合法手マスク (学習時に非合法手を無視するため)
"""

from __future__ import annotations
import random
import numpy as np
from dataclasses import dataclass
from typing import Optional
from startups import StartupsGame, NUM_PLAYERS
from encoding import encode_observation, get_legal_action_mask
from network import PolicyValueNet
from az_ismcts import AlphaZeroISMCTS


@dataclass
class TrainingSample:
    state: np.ndarray        # (OBSERVATION_SIZE,)
    policy: np.ndarray       # (ACTION_SIZE,)
    value: float             # [-1, 0, 1]
    legal_mask: np.ndarray   # (ACTION_SIZE,)


def self_play_one_game(
    net: PolicyValueNet,
    iterations: int = 100,
    rng: Optional[random.Random] = None,
    temperature_moves: int = 10,
) -> tuple[list[TrainingSample], list[float]]:
    """1ゲーム自己対戦し、学習サンプルと最終報酬を返す。

    Args:
        net: 使用するネットワーク
        iterations: MCTSイテレーション数
        rng: 乱数生成器
        temperature_moves: 最初の N 手はサンプリング (探索の多様性)、以降は argmax

    Returns:
        samples: この試合から得られた学習サンプル
        rewards: 各プレイヤーの最終コイン
    """
    if rng is None:
        rng = random.Random()

    game = StartupsGame(seed=rng.randint(0, 10**9))

    # 3人それぞれに別のMCTSエージェントを用意 (Dirichletノイズの乱数分離)
    agents = [
        AlphaZeroISMCTS(
            net=net,
            iterations=iterations,
            rng=random.Random(rng.randint(0, 10**9)),
            add_dirichlet_noise=True,
        )
        for _ in range(NUM_PLAYERS)
    ]

    # 各プレイヤー視点の (state, policy, mask) を貯めるバッファ
    # ゲーム終了後に value を追記して Sample 化
    pending = [[] for _ in range(NUM_PLAYERS)]  # list[list[(state, policy, mask)]]
    move_count = 0

    while not game.is_terminal():
        pid = game.current_player()
        obs = game.get_observation(pid)
        state_vec = encode_observation(obs)
        mask = get_legal_action_mask(game)

        action, policy_vec = agents[pid].search(
            game, root_player=pid, return_policy=True
        )

        pending[pid].append((state_vec, policy_vec, mask))

        # 温度制御: 最初の数手は policy からサンプリング、以降は argmax
        if move_count < temperature_moves:
            # policy が完全に0なら action (MCTS 選択) をそのまま使う
            if policy_vec.sum() > 0:
                sampled_idx = np.random.choice(len(policy_vec), p=policy_vec)
                # sampled_idx を実際の手に変換
                from encoding import get_legal_action_map
                action_map = get_legal_action_map(game)
                if sampled_idx in action_map:
                    action = action_map[sampled_idx]
        # それ以外は agent.search が返した argmax の action をそのまま使う

        game.step(action)
        move_count += 1

    # 勝敗から各プレイヤーの value を決定 (ポイント制)
    rewards = game.get_rewards()  # [2, 1, -1]
    point_to_value = {2: 1.0, 1: 0.0, -1: -1.0}
    values = [point_to_value.get(rewards[pid], 0.0) for pid in range(NUM_PLAYERS)]

    # サンプル化
    samples = []
    for pid in range(NUM_PLAYERS):
        for state, policy, mask in pending[pid]:
            samples.append(TrainingSample(
                state=state,
                policy=policy,
                value=values[pid],
                legal_mask=mask,
            ))

    return samples, rewards


def self_play_many(
    net: PolicyValueNet,
    num_games: int,
    iterations: int = 100,
    seed: int = 0,
) -> list[TrainingSample]:
    """複数ゲーム自己対戦してサンプルをまとめて返す。"""
    rng = random.Random(seed)
    all_samples = []
    for g in range(num_games):
        samples, rewards = self_play_one_game(net, iterations=iterations, rng=rng)
        all_samples.extend(samples)
        if (g + 1) % max(1, num_games // 5) == 0:
            print(f"  self-play {g+1}/{num_games} done, rewards={rewards}, samples so far={len(all_samples)}")
    return all_samples


# ============================================================
# 動作確認
# ============================================================

if __name__ == "__main__":
    import time

    net = PolicyValueNet(hidden=64, num_layers=2)

    print("=== 1ゲーム自己対戦 ===")
    start = time.time()
    samples, rewards = self_play_one_game(net, iterations=50, rng=random.Random(0))
    elapsed = time.time() - start
    print(f"所要時間: {elapsed:.1f}秒")
    print(f"得られたサンプル数: {len(samples)}")
    print(f"最終報酬: {rewards}")

    # サンプルの中身をざっと確認
    s = samples[0]
    print(f"\n最初のサンプル:")
    print(f"  state shape: {s.state.shape}")
    print(f"  policy: {s.policy} (合計: {s.policy.sum():.3f})")
    print(f"  value: {s.value}")
    print(f"  legal_mask sum: {int(s.legal_mask.sum())}")
