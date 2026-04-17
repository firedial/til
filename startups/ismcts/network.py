"""
Policy-Value Network for スタータップス AlphaZero風学習。

ネットワーク構造:
  入力 (OBSERVATION_SIZE=67)
    → 共通 Trunk (MLP)
    → Policy Head: ACTION_SIZE=19 のロジット
    → Value Head: スカラー [-1, 1] (tanh活性化)

AlphaZero論文ではCNNだが、スタータップスは盤面ではないので単純なMLPで十分。
"""

from __future__ import annotations
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from encoding import OBSERVATION_SIZE, ACTION_SIZE


class PolicyValueNet(nn.Module):
    """Policy と Value の 2 ヘッド出力 MLP。"""

    def __init__(self, hidden: int = 128, num_layers: int = 3):
        super().__init__()
        layers = []
        in_dim = OBSERVATION_SIZE
        for _ in range(num_layers):
            layers.append(nn.Linear(in_dim, hidden))
            layers.append(nn.ReLU())
            in_dim = hidden
        self.trunk = nn.Sequential(*layers)
        # Policy Head: 合法手マスクを適用する前の生ロジット
        self.policy_head = nn.Linear(hidden, ACTION_SIZE)
        # Value Head: 勝率 (-1 ～ +1)
        self.value_head = nn.Sequential(
            nn.Linear(hidden, hidden // 2),
            nn.ReLU(),
            nn.Linear(hidden // 2, 1),
            nn.Tanh(),
        )

    def forward(self, x: torch.Tensor):
        """
        Args:
            x: (batch, OBSERVATION_SIZE) のテンソル
        Returns:
            policy_logits: (batch, ACTION_SIZE)
            value:         (batch, 1) in [-1, 1]
        """
        h = self.trunk(x)
        return self.policy_head(h), self.value_head(h)

    @torch.no_grad()
    def predict(
        self,
        obs_vec: np.ndarray,
        legal_mask: np.ndarray,
    ) -> tuple[np.ndarray, float]:
        """推論: 単一の観測ベクトルから (policy, value) を返す。

        Args:
            obs_vec: (OBSERVATION_SIZE,)
            legal_mask: (ACTION_SIZE,)  合法手のみ1

        Returns:
            policy: (ACTION_SIZE,) 合法手のみ正の値を持つ確率分布
            value:  スカラー [-1, 1]
        """
        self.eval()
        x = torch.from_numpy(obs_vec).float().unsqueeze(0)  # (1, D)
        logits, v = self.forward(x)
        logits = logits.squeeze(0).numpy()           # (ACTION_SIZE,)
        value = float(v.squeeze().item())

        # 合法手マスクを適用してソフトマックス
        # 非合法手はロジット -inf に
        masked = np.where(legal_mask > 0, logits, -1e9)
        # 数値安定化
        masked -= masked.max()
        probs = np.exp(masked) * (legal_mask > 0)
        s = probs.sum()
        if s > 0:
            probs = probs / s
        else:
            # フォールバック(起きないはず)
            probs = legal_mask / max(1.0, legal_mask.sum())
        return probs, value


# ============================================================
# 動作確認
# ============================================================

if __name__ == "__main__":
    from startups import StartupsGame
    from encoding import encode_observation, get_legal_action_mask
    import random

    net = PolicyValueNet(hidden=64, num_layers=2)
    n_params = sum(p.numel() for p in net.parameters())
    print(f"モデルパラメータ数: {n_params:,}")

    # 1ゲーム進めて推論してみる
    game = StartupsGame(seed=0)
    rng = random.Random(0)
    for _ in range(3):
        if game.is_terminal():
            break
        actions = game.get_legal_actions()
        game.step(rng.choice(actions))

    obs = game.get_observation(0)
    vec = encode_observation(obs)
    mask = get_legal_action_mask(game)

    policy, value = net.predict(vec, mask)
    print(f"\n推論結果:")
    print(f"  policy: {policy}")
    print(f"  value: {value:.4f}")
    print(f"  policy は合法手のみ非0? {(policy[mask==0] == 0).all()}")
    print(f"  policy の合計: {policy.sum():.4f} (1になるはず)")

    # バッチ推論もテスト
    print(f"\n=== バッチ推論テスト ===")
    batch = torch.randn(32, OBSERVATION_SIZE)
    logits, values = net(batch)
    print(f"  policy logits shape: {logits.shape}")
    print(f"  values shape: {values.shape}")
    print(f"  value range: [{values.min().item():.3f}, {values.max().item():.3f}] (tanh なので [-1,1])")
