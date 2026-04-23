"""
NN の訓練ループ。

1エポックの流れ:
  1. 自己対戦で大量のサンプルを集める
  2. サンプルをシャッフルしてミニバッチを作成
  3. 各ミニバッチで NN を更新 (Adam で)
  4. エポックごとに評価 (旧ネットワーク or ISMCTSと対戦)
"""

from __future__ import annotations
import random
import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
from network import PolicyValueNet
from self_play import self_play_many, TrainingSample
from encoding import OBSERVATION_SIZE, ACTION_SIZE


def samples_to_tensors(samples: list[TrainingSample]):
    """サンプルリストを PyTorch テンソルに変換。"""
    states = np.stack([s.state for s in samples])
    policies = np.stack([s.policy for s in samples])
    values = np.array([s.value for s in samples], dtype=np.float32)
    masks = np.stack([s.legal_mask for s in samples])
    return (
        torch.from_numpy(states).float(),
        torch.from_numpy(policies).float(),
        torch.from_numpy(values).float(),
        torch.from_numpy(masks).float(),
    )


def train_epoch(
    net: PolicyValueNet,
    samples: list[TrainingSample],
    epochs: int = 3,
    batch_size: int = 128,
    lr: float = 1e-3,
    device: str = "cpu",
) -> dict:
    """サンプル群で NN を訓練。損失履歴を返す。"""
    net.to(device)
    net.train()

    states, policies, values, masks = samples_to_tensors(samples)
    dataset = TensorDataset(states, policies, values, masks)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    optimizer = torch.optim.Adam(net.parameters(), lr=lr, weight_decay=1e-4)

    history = {"loss": [], "policy_loss": [], "value_loss": []}

    for ep in range(epochs):
        ep_loss = ep_pl = ep_vl = 0.0
        n_batches = 0
        for s, p, v, m in loader:
            s, p, v, m = s.to(device), p.to(device), v.to(device), m.to(device)
            logits, pred_v = net(s)
            pred_v = pred_v.squeeze(-1)

            # 非合法手をマスク: m=0 の位置を -1e9 に(-infはNaNの原因になる)
            masked_logits = logits.clone()
            masked_logits[m == 0] = -1e9
            log_probs = F.log_softmax(masked_logits, dim=1)

            # ポリシー損失: 交差エントロピー
            # p はターゲット分布 (訪問回数比率)、log_probs はモデルの log-softmax
            # 非合法手は p=0 かつ log_probs=約-1e9 なので、積が -0*1e9=0 (nan 回避)
            # さらに念のため p > 0 の位置のみ計算する
            policy_loss = -(p * log_probs * m).sum(dim=1).mean()

            # 価値損失: MSE
            value_loss = F.mse_loss(pred_v, v)

            loss = policy_loss + value_loss
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            ep_loss += loss.item()
            ep_pl += policy_loss.item()
            ep_vl += value_loss.item()
            n_batches += 1

        avg_loss = ep_loss / max(1, n_batches)
        avg_pl = ep_pl / max(1, n_batches)
        avg_vl = ep_vl / max(1, n_batches)
        history["loss"].append(avg_loss)
        history["policy_loss"].append(avg_pl)
        history["value_loss"].append(avg_vl)
        print(f"  epoch {ep+1}/{epochs}: loss={avg_loss:.4f} (policy={avg_pl:.4f}, value={avg_vl:.4f})")

    return history


def training_loop(
    net: PolicyValueNet,
    num_iterations: int = 5,
    games_per_iter: int = 20,
    mcts_iters: int = 50,
    epochs_per_iter: int = 3,
    batch_size: int = 128,
    lr: float = 1e-3,
):
    """学習の全体ループ。

    各イテレーション:
      1. 自己対戦でサンプルを集める
      2. サンプルで NN を更新
    """
    all_samples = []  # 経験バッファ (古いサンプルも混ぜる方が安定)
    max_buffer = 10000  # 経験バッファの最大サイズ

    for it in range(num_iterations):
        print(f"\n========== Iteration {it+1}/{num_iterations} ==========")
        print(f"[Self-play] {games_per_iter} games, {mcts_iters} MCTS iters each")
        start = time.time()
        new_samples = self_play_many(
            net, num_games=games_per_iter, iterations=mcts_iters, seed=it * 1000
        )
        t_sp = time.time() - start
        print(f"  -> {len(new_samples)} samples in {t_sp:.1f}s")

        # 経験バッファに追加 (最新のサンプルを重視しつつ古いものも残す)
        all_samples.extend(new_samples)
        if len(all_samples) > max_buffer:
            all_samples = all_samples[-max_buffer:]

        print(f"[Train] {len(all_samples)} samples total, {epochs_per_iter} epochs")
        start = time.time()
        train_epoch(
            net,
            all_samples,
            epochs=epochs_per_iter,
            batch_size=batch_size,
            lr=lr,
        )
        t_tr = time.time() - start
        print(f"  -> trained in {t_tr:.1f}s")


if __name__ == "__main__":
    # 軽量な学習ループを実行
    net = PolicyValueNet(hidden=64, num_layers=2)
    training_loop(
        net,
        num_iterations=2,
        games_per_iter=5,
        mcts_iters=30,
        epochs_per_iter=2,
        batch_size=64,
    )

    # 保存
    torch.save(net.state_dict(), "/home/claude/az_net_smoke.pt")
    print("\n保存: /home/claude/az_net_smoke.pt")
