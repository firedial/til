"""
ISMCTS vs ベースライン(Random, Greedy)の強さ測定。
"""

import random
import time
from startups import StartupsGame, NUM_PLAYERS
from ismcts import ISMCTS
from test_random import random_policy, greedy_policy


def ismcts_policy_factory(iterations: int = 500, seed: int = 0):
    """ISMCTS を policy function (game, rng) -> action として使えるようにする。"""
    agent = ISMCTS(iterations=iterations, rng=random.Random(seed))

    def policy(game, rng):
        root_player = game.current_player()
        return agent.search(game, root_player)

    return policy


def play_one_game(policies: list, seed: int) -> list[float]:
    game = StartupsGame(seed=seed)
    rng = random.Random(seed + 9999)
    steps = 0
    while not game.is_terminal() and steps < 2000:
        pid = game.current_player()
        action = policies[pid](game, rng)
        game.step(action)
        steps += 1
    return game.get_rewards()


def tournament(policies, num_games: int, base_seed: int = 0, label: str = ""):
    wins = [0] * NUM_PLAYERS
    draws = 0
    total_coins = [0.0] * NUM_PLAYERS

    start = time.time()
    for g in range(num_games):
        rewards = play_one_game(policies, base_seed + g)
        for i, r in enumerate(rewards):
            total_coins[i] += r
        m = max(rewards)
        top = [i for i, r in enumerate(rewards) if r == m]
        if len(top) == 1:
            wins[top[0]] += 1
        else:
            draws += 1
        # 進捗表示
        if (g + 1) % max(1, num_games // 10) == 0:
            print(f"  [{label}] {g+1}/{num_games} games done...")

    elapsed = time.time() - start
    print(f"\n=== {label} ({num_games} games, {elapsed:.1f}s) ===")
    for i in range(NUM_PLAYERS):
        wr = wins[i] / num_games * 100
        avg = total_coins[i] / num_games
        print(f"  P{i}: wins={wins[i]} ({wr:.1f}%), avg_coins={avg:.2f}")
    print(f"  Draws: {draws}")
    return wins, draws, total_coins


if __name__ == "__main__":
    # ============================================================
    # 実験1: ISMCTS(P0) vs Random(P1) vs Random(P2)
    # ============================================================
    print("===== 実験1: ISMCTS vs Random vs Random =====")
    ismcts_pol = ismcts_policy_factory(iterations=300, seed=0)
    tournament(
        [ismcts_pol, random_policy, random_policy],
        num_games=50,
        base_seed=0,
        label="ISMCTS vs Rand vs Rand",
    )

    # ============================================================
    # 実験2: ISMCTS(P0) vs Greedy(P1) vs Greedy(P2)
    # ============================================================
    print("\n\n===== 実験2: ISMCTS vs Greedy vs Greedy =====")
    ismcts_pol2 = ismcts_policy_factory(iterations=3000, seed=1)
    tournament(
        [ismcts_pol2, greedy_policy, greedy_policy],
        num_games=50,
        base_seed=1000,
        label="ISMCTS vs Greedy vs Greedy",
    )

    # ============================================================
    # 実験3: ISMCTS 同士の対戦 (3体とも)
    # ============================================================
    # ISMCTSを複数使うと遅いので少なめの iterations + 少ないゲーム数
    print("\n\n===== 実験3: ISMCTS vs ISMCTS vs ISMCTS (軽量版) =====")
    i1 = ismcts_policy_factory(iterations=100, seed=10)
    i2 = ismcts_policy_factory(iterations=100, seed=20)
    i3 = ismcts_policy_factory(iterations=100, seed=30)
    tournament(
        [i1, i2, i3],
        num_games=20,
        base_seed=2000,
        label="ISMCTS x3",
    )
