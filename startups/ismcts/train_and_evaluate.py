"""
学習前 (ランダム重み) vs 学習後 の NN を使った
AlphaZero ISMCTS 同士を対戦させて、学習効果を確認する。

- P0: 訓練後のNN (trained)
- P1, P2: 訓練前のNN (untrained)
"""

import random
import time
import torch
import copy
from startups import StartupsGame, NUM_PLAYERS
from network import PolicyValueNet
from az_ismcts import AlphaZeroISMCTS
from self_play import self_play_many
from train import train_epoch


def play_one_game(policies, seed):
    game = StartupsGame(seed=seed)
    steps = 0
    while not game.is_terminal() and steps < 2000:
        pid = game.current_player()
        action = policies[pid](game)
        game.step(action)
        steps += 1
    return game.get_rewards()


def make_policy_from_net(net, iterations=50, seed=0):
    agent = AlphaZeroISMCTS(
        net=net, iterations=iterations, rng=random.Random(seed)
    )
    def policy(game):
        return agent.search(game, root_player=game.current_player())
    return policy


def tournament(policies, num_games, base_seed=0, label=""):
    wins = [0] * NUM_PLAYERS
    draws = 0
    coins_sum = [0.0] * NUM_PLAYERS
    for g in range(num_games):
        rewards = play_one_game(policies, base_seed + g)
        for i, r in enumerate(rewards):
            coins_sum[i] += r
        m = max(rewards)
        top = [i for i, r in enumerate(rewards) if r == m]
        if len(top) == 1:
            wins[top[0]] += 1
        else:
            draws += 1
    print(f"\n=== {label} ({num_games} games) ===")
    for i in range(NUM_PLAYERS):
        print(f"  P{i}: wins={wins[i]} ({wins[i]/num_games*100:.1f}%), avg_coins={coins_sum[i]/num_games:.2f}")
    print(f"  Draws: {draws}")
    return wins


if __name__ == "__main__":
    # untrained なNNを保存
    untrained = PolicyValueNet(hidden=64, num_layers=2)
    # trained 用にコピーを作り、学習させる
    trained = PolicyValueNet(hidden=64, num_layers=2)
    trained.load_state_dict(untrained.state_dict())

    # ------------ まず学習 ------------
    print(">>> 学習を実施します")
    rng = random.Random(0)
    all_samples = []
    NUM_ITER = 20
    GAMES_PER_ITER = 30
    MCTS_ITERS = 200

    for it in range(NUM_ITER):
        print(f"\n--- Iteration {it+1}/{NUM_ITER} ---")
        start = time.time()
        samples = self_play_many(
            trained, num_games=GAMES_PER_ITER, iterations=MCTS_ITERS, seed=it * 10000
        )
        print(f"  self-play: {len(samples)} samples, {time.time()-start:.1f}s")
        all_samples.extend(samples)
        if len(all_samples) > 8000:
            all_samples = all_samples[-8000:]
        start = time.time()
        train_epoch(trained, all_samples, epochs=3, batch_size=128, lr=1e-3)
        print(f"  train: {time.time()-start:.1f}s")

    # 保存
    torch.save(trained.state_dict(), "./az_net_trained.pt")
    torch.save(untrained.state_dict(), "./az_net_untrained.pt")

    # ------------ 対戦 ------------
    print("\n\n>>> trained(P0) vs untrained(P1,P2) で対戦")
    trained_pol = make_policy_from_net(trained, iterations=40, seed=100)
    untrained_pol1 = make_policy_from_net(untrained, iterations=40, seed=200)
    untrained_pol2 = make_policy_from_net(untrained, iterations=40, seed=300)
    tournament(
        [trained_pol, untrained_pol1, untrained_pol2],
        num_games=30,
        base_seed=99999,
        label="Trained vs Untrained x 2",
    )
