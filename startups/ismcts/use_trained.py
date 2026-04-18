"""
学習済みモデルを使う最小サンプル。

使い方:
    python use_trained.py

やっていること:
  1. 学習済みの重みをロード
  2. それを使って ISMCTS エージェントを作成
  3. 1ゲーム詳細表示で進める (AI同士の対戦)
"""

import random
import torch
from startups import StartupsGame
from network import PolicyValueNet
from az_ismcts import AlphaZeroISMCTS


def main():
    # 1. モデルをロード
    net = PolicyValueNet(hidden=64, num_layers=2)
    net.load_state_dict(torch.load("az_net_trained.pt", weights_only=True))
    net.eval()
    print("✅ 学習済みモデルをロードしました")

    # 2. 3人分のエージェントを作成 (全員同じ学習済みNN使用)
    agents = [
        AlphaZeroISMCTS(
            net=net, iterations=100, rng=random.Random(i * 7 + 1)
        )
        for i in range(3)
    ]

    # 3. 1ゲーム詳細表示で進める
    game = StartupsGame(seed=42)
    print("\n=== ゲーム開始 ===")
    print(game.render())

    step = 0
    while not game.is_terminal():
        pid = game.current_player()
        action = agents[pid].search(game, root_player=pid)
        print(f"\n--- Step {step}: P{pid} が {action} を選択 ---")
        game.step(action)
        step += 1
        if step > 200:
            print("(手数が多いので以降省略)")
            break

    print("\n=== 最終結果 ===")
    print(game.render())
    coins = game.get_rewards()
    winner = game.get_winner()
    print(f"\n最終コイン: {coins}")
    if winner is not None:
        print(f"勝者: P{winner}")
    else:
        print(f"引き分け")


if __name__ == "__main__":
    main()
