"""
AlphaZero 風の ISMCTS (NN 統合版)。

通常の ISMCTS との違い:
  - ロールアウトしない代わりに、NN の value を使う
  - UCB1 の代わりに PUCT (Predictor + UCT) を使う
  - NN の policy を「事前確率 P」として探索のガイドに

PUCT:
    score(a) = Q(a) + c_puct * P(a) * sqrt(N_parent) / (1 + N_child(a))

ここで:
    Q(a) = child.total_value / child.visits  (a を選んだ後の平均価値)
    P(a) = NN policy の出力 (合法手に正規化済み)
    N_parent = その選択肢が出現した回数の合計
    N_child = その選択肢が選ばれた回数
"""

from __future__ import annotations
import math
import random
from typing import Optional
import numpy as np
import torch
from startups import StartupsGame, NUM_PLAYERS
from determinize import determinize_from_observation
from encoding import (
    encode_observation,
    get_legal_action_mask,
    get_legal_action_map,
    action_to_index_with_game,
    ACTION_SIZE,
)
from network import PolicyValueNet


class AZNode:
    """AlphaZero 風 ISMCTS のノード。

    各子は action index (int) でキー付け。
    """
    __slots__ = (
        "parent",
        "incoming_action_idx",
        "children",        # dict[int, AZNode]
        "prior",           # dict[int, float]  NN からの事前確率
        "visits",          # dict[int, int]    各子アクションの訪問回数
        "value_sum",       # dict[int, float]  各子アクションの累積価値
        "availability",    # dict[int, int]    各子アクションが選択肢に出た回数
        "total_visits",    # このノードを通過した回数
        "expanded",        # このノードで NN 推論済みか
    )

    def __init__(
        self,
        parent: Optional["AZNode"],
        incoming_action_idx: Optional[int],
    ):
        self.parent = parent
        self.incoming_action_idx = incoming_action_idx
        self.children = {}
        self.prior = {}
        self.visits = {}
        self.value_sum = {}
        self.availability = {}
        self.total_visits = 0
        self.expanded = False


class AlphaZeroISMCTS:
    """AlphaZero 風 ISMCTS エージェント。"""

    def __init__(
        self,
        net: PolicyValueNet,
        iterations: int = 200,
        c_puct: float = 1.5,
        rng: Optional[random.Random] = None,
        add_dirichlet_noise: bool = False,
        dirichlet_alpha: float = 0.3,
        dirichlet_epsilon: float = 0.25,
    ):
        """
        Args:
            net: PolicyValueNet (推論に使用)
            iterations: 1手決めるための探索回数
            c_puct: PUCT 探索係数
            rng: 乱数生成器
            add_dirichlet_noise: ルートでDirichletノイズを加えるか (探索促進、自己対戦で有用)
            dirichlet_alpha, dirichlet_epsilon: ノイズパラメータ
        """
        self.net = net
        self.iterations = iterations
        self.c_puct = c_puct
        self.rng = rng or random.Random()
        self.add_dirichlet_noise = add_dirichlet_noise
        self.dirichlet_alpha = dirichlet_alpha
        self.dirichlet_epsilon = dirichlet_epsilon

    def search(
        self,
        game: StartupsGame,
        root_player: int,
        return_policy: bool = False,
        return_stats: bool = False,
    ):
        """与えられた局面から最善手を探索して返す。

        Args:
            game: 現在のゲーム状態
            root_player: どのプレイヤー視点か
            return_policy: True なら (action, policy_vector) のタプルを返す。
            return_stats: True なら (action, stats_dict) のタプルを返す。
                          stats_dict は {action_index: {visits, winrate, action_tuple}} の辞書。

        Returns:
            action (tuple) または (action, policy_vector) または (action, stats_dict)
        """
        obs = game.get_observation(root_player)
        root = AZNode(parent=None, incoming_action_idx=None)

        for _ in range(self.iterations):
            det_game = determinize_from_observation(obs, self.rng)
            self._simulate(det_game, root, root_player, is_root=True)

        # 最終選択: 訪問回数最大の手
        if not root.visits:
            actions = game.get_legal_actions()
            chosen = self.rng.choice(actions)
            if return_policy:
                return chosen, np.zeros(ACTION_SIZE, dtype=np.float32)
            if return_stats:
                return chosen, {}
            return chosen

        # 現実の game (決定化前) での合法手マップを使う
        action_map = get_legal_action_map(game)

        best_idx = max(root.visits.items(), key=lambda kv: kv[1])[0]
        if best_idx in action_map:
            chosen_action = action_map[best_idx]
        else:
            chosen_action = self.rng.choice(list(action_map.values()))

        if return_policy:
            policy_vec = np.zeros(ACTION_SIZE, dtype=np.float32)
            total = sum(root.visits.values())
            if total > 0:
                for idx, n in root.visits.items():
                    policy_vec[idx] = n / total
            return chosen_action, policy_vec

        if return_stats:
            stats = {}
            for idx, action_tuple in action_map.items():
                visits = root.visits.get(idx, 0)
                value_sum = root.value_sum.get(idx, 0.0)
                # Q値: [-1, 1] の平均。-1=3位, 0=2位, 1=1位
                q = (value_sum / visits) if visits > 0 else 0.0
                # Q値を順位ポイント期待値に変換
                # Q=-1 → -1pt(3位), Q=0 → 1pt(2位), Q=1 → 2pt(1位)
                # 線形補間: expected_points = q * 1.5 + 0.5
                # (Q=-1→-1, Q=0→0.5, Q=1→2) ... これは近似。
                # より正確には、3位=-1, 2位=1, 1位=2 として:
                # P(1st) ≈ (q+1)/2 の上側, P(3rd) ≈ (1-q)/2 の下側
                # 簡易計算: ep = P(1st)*2 + P(2nd)*1 + P(3rd)*(-1)
                # P(1st)=(q+1)/2, P(3rd)=(1-q)/2, P(2nd)=1-P(1st)-P(3rd)
                p1 = max(0, min(1, (q + 1) / 2))  # 1位確率
                p3 = max(0, min(1, (1 - q) / 2))   # 3位確率
                p2 = max(0, 1 - p1 - p3)            # 2位確率
                ep = p1 * 2 + p2 * 1 + p3 * (-1)
                stats[idx] = {
                    "visits": visits,
                    "q": round(q, 4),
                    "expected_points": round(ep, 2),
                    "action": action_tuple,
                }
            return chosen_action, stats

        return chosen_action

    def _simulate(
        self,
        det_game: StartupsGame,
        root: AZNode,
        root_player: int,
        is_root: bool,
    ):
        """1回分のシミュレーション (Select → Expand → Backup)。"""
        node = root
        path = []  # (node, action_idx) のリスト。Backupで使う

        while not det_game.is_terminal():
            # まだノードが NN 推論されていなければ展開して抜ける (Expand)
            if not node.expanded:
                self._expand(node, det_game, is_root=is_root and (node is root))
                # 葉ノードの NN value を使って Backup
                vec = encode_observation(det_game.get_observation(root_player))
                mask = get_legal_action_mask(det_game)
                _, value = self.net.predict(vec, mask)
                self._backup(path, root, value)
                return

            # 既に展開済み → PUCT で選択
            legal = det_game.get_legal_actions()
            legal_indices = [action_to_index_with_game(a, det_game) for a in legal]

            # availability を更新
            for idx in legal_indices:
                node.availability[idx] = node.availability.get(idx, 0) + 1

            chosen_idx = self._puct_select(node, legal_indices)
            # chosen_idx を実際の行動に変換 (legal の中から)
            chosen_action = None
            for a, idx in zip(legal, legal_indices):
                if idx == chosen_idx:
                    chosen_action = a
                    break

            det_game.step(chosen_action)
            path.append((node, chosen_idx))

            # 子ノードがなければ作る
            if chosen_idx not in node.children:
                node.children[chosen_idx] = AZNode(
                    parent=node, incoming_action_idx=chosen_idx
                )
            node = node.children[chosen_idx]
            is_root = False

        # 終端に到達 → ポイント制報酬で Backup
        rewards = det_game.get_rewards()  # [2, 1, -1]
        my_points = rewards[root_player]
        # 正規化: 1位→1.0, 2位→0.0, 3位→-1.0
        value = {2: 1.0, 1: 0.0, -1: -1.0}.get(my_points, 0.0)

        self._backup(path, root, value)

    def _expand(self, node: AZNode, det_game: StartupsGame, is_root: bool):
        """ノードを NN で展開 (事前確率を設定)。"""
        obs = det_game.get_observation(det_game.current_player())
        vec = encode_observation(obs)
        mask = get_legal_action_mask(det_game)
        policy, _ = self.net.predict(vec, mask)

        if is_root and self.add_dirichlet_noise:
            # ルートのみ Dirichlet ノイズを加える (AlphaZero 流)
            legal_idx = np.where(mask > 0)[0]
            if len(legal_idx) > 1:
                noise = np.random.dirichlet([self.dirichlet_alpha] * len(legal_idx))
                for i, idx in enumerate(legal_idx):
                    policy[idx] = (
                        (1 - self.dirichlet_epsilon) * policy[idx]
                        + self.dirichlet_epsilon * noise[i]
                    )

        for idx in range(ACTION_SIZE):
            if mask[idx] > 0:
                node.prior[idx] = float(policy[idx])
                node.visits.setdefault(idx, 0)
                node.value_sum.setdefault(idx, 0.0)
                node.availability.setdefault(idx, 0)
        node.expanded = True

    def _puct_select(self, node: AZNode, legal_indices: list[int]) -> int:
        """PUCT で action index を1つ選ぶ。"""
        total_n = max(1, sum(node.visits.get(idx, 0) for idx in legal_indices))
        sqrt_total = math.sqrt(total_n)

        best_idx = legal_indices[0]
        best_score = -float("inf")
        for idx in legal_indices:
            n = node.visits.get(idx, 0)
            if n > 0:
                q = node.value_sum[idx] / n
            else:
                q = 0.0
            p = node.prior.get(idx, 1.0 / max(1, len(legal_indices)))
            u = self.c_puct * p * sqrt_total / (1 + n)
            score = q + u
            if score > best_score:
                best_score = score
                best_idx = idx
        return best_idx

    def _backup(self, path: list, root: AZNode, value: float):
        """path を逆順に辿って訪問回数と累積価値を更新。"""
        for node, idx in path:
            node.total_visits += 1
            node.visits[idx] = node.visits.get(idx, 0) + 1
            node.value_sum[idx] = node.value_sum.get(idx, 0.0) + value
        root.total_visits += 1


# ============================================================
# 動作確認
# ============================================================

if __name__ == "__main__":
    import time

    net = PolicyValueNet(hidden=64, num_layers=2)
    agent = AlphaZeroISMCTS(net=net, iterations=100, rng=random.Random(0))

    game = StartupsGame(seed=42)
    # 数手進めて判断できる場面を作る
    rng = random.Random(100)
    for _ in range(5):
        if game.is_terminal():
            break
        a = rng.choice(game.get_legal_actions())
        game.step(a)

    print("=== 現在の局面 ===")
    print(game.render())

    start = time.time()
    action, policy = agent.search(game, root_player=game.current_player(), return_policy=True)
    elapsed = time.time() - start

    print(f"\n選択した行動: {action}")
    print(f"探索ポリシー (訪問回数ベース): {policy}")
    print(f"所要時間: {elapsed:.2f}秒")
