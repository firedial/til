"""
ISMCTS (Information Set Monte Carlo Tree Search) の実装。

参考文献:
  Cowling, P. I., Powley, E. J., & Whitehouse, D. (2012).
  "Information Set Monte Carlo Tree Search."
  IEEE Transactions on Computational Intelligence and AI in Games.

本実装は SO-ISMCTS (Single-Observer ISMCTS) と呼ばれる最もシンプルな版:
  - 木は「探索する側のプレイヤーから見た行動」をノードとして持つ
  - 各シミュレーションで世界を1つ決定化 (determinize)
  - 決定化した世界で合法な手だけを辿る
  - 合法性チェックがあるため、未訪問の手でも決定化によっては使えない

アルゴリズム (1回分の iteration):
  1. 現在の観測から世界をサンプリング (determinize)
  2. ルートから、「決定化世界で合法 かつ UCB1 最大」な子を辿る
  3. 未訪問の合法手があれば展開 (expand)
  4. 残りはランダムプレイアウト (rollout)
  5. 結果を逆伝播 (backpropagate)

iteration を N 回繰り返した後、「訪問回数が最も多い手」を最終的な選択とする。
"""

from __future__ import annotations
import math
import random
from typing import Optional
from startups import StartupsGame, NUM_PLAYERS
from determinize import determinize_from_observation


# ============================================================
# ノード定義
# ============================================================

class ISMCTSNode:
    """ISMCTS の木のノード。

    Attributes:
        parent: 親ノード (Noneならroot)
        incoming_action: このノードに辿り着くための行動
        children: {action: ISMCTSNode} の辞書
        visits: このノードを通過した回数
        total_reward: このノードから得た累積報酬 (探索プレイヤー視点)
        availability: このノードの「親から見て、選択肢として出現した」回数
                      (選択肢に出ない=決定化で合法でない時は数えない。UCB1の分母で使う)
        player_to_move: このノードで行動するプレイヤー
    """

    __slots__ = (
        "parent",
        "incoming_action",
        "children",
        "visits",
        "total_reward",
        "availability",
        "player_to_move",
    )

    def __init__(
        self,
        parent: Optional["ISMCTSNode"],
        incoming_action: Optional[tuple],
        player_to_move: int,
    ):
        self.parent = parent
        self.incoming_action = incoming_action
        self.children: dict[tuple, "ISMCTSNode"] = {}
        self.visits = 0
        self.total_reward = 0.0
        self.availability = 0
        self.player_to_move = player_to_move

    def is_leaf_for(self, legal_actions: list[tuple]) -> bool:
        """決定化世界で合法な手のうち、未展開の手があれば True。"""
        for a in legal_actions:
            if a not in self.children:
                return True
        return False

    def untried_actions(self, legal_actions: list[tuple]) -> list[tuple]:
        return [a for a in legal_actions if a not in self.children]


# ============================================================
# 報酬整形
# ============================================================

def compute_reward_for(
    game: StartupsGame,
    root_player: int,
) -> float:
    """root_player 視点の報酬を返す。

    get_rewards() は [2, 1, -1] のポイント制。
    MCTS用に [-1, 1] に正規化する:
      1位(2点) → 1.0
      2位(1点) → 0.0
      3位(-1点) → -1.0
    """
    rewards = game.get_rewards()
    my_points = rewards[root_player]
    if my_points == 2:
        return 1.0
    elif my_points == 1:
        return 0.0
    else:
        return -1.0


# ============================================================
# ISMCTS 本体
# ============================================================

class ISMCTS:
    """ISMCTS エージェント。

    使い方:
        agent = ISMCTS(iterations=1000)
        action = agent.search(game, root_player)
    """

    def __init__(
        self,
        iterations: int = 1000,
        c_uct: float = 0.7,
        rng: Optional[random.Random] = None,
    ):
        """
        Args:
            iterations: 1手決めるためのシミュレーション回数
            c_uct: UCB1 の探索係数 (大きいほど未探索を試す)
            rng: 乱数生成器
        """
        self.iterations = iterations
        self.c_uct = c_uct
        self.rng = rng or random.Random()

    def search(self, game: StartupsGame, root_player: int) -> tuple:
        """game の現局面から root_player の最善手を返す。"""
        # 観測を取得
        obs = game.get_observation(root_player)

        # ルートノード作成
        root = ISMCTSNode(
            parent=None,
            incoming_action=None,
            player_to_move=obs["current_player"],
        )

        for _ in range(self.iterations):
            # 1. 決定化: この iteration での「世界」を確定
            det_game = determinize_from_observation(obs, self.rng)
            # 2-4. 1回のシミュレーション
            self._simulate(det_game, root, root_player)

        # 最終選択: 訪問回数最大の手
        if not root.children:
            # 探索が何も試せなかった (通常ありえないが念のため)
            actions = game.get_legal_actions()
            return self.rng.choice(actions)

        best_action = max(root.children.items(), key=lambda kv: kv[1].visits)[0]
        return best_action

    def _simulate(
        self,
        det_game: StartupsGame,
        root: ISMCTSNode,
        root_player: int,
    ):
        """1回分の iteration (Selection → Expansion → Rollout → Backprop)。"""
        node = root
        path = [node]

        # -------- Selection + Expansion --------
        while not det_game.is_terminal():
            legal = det_game.get_legal_actions()
            # 合法手のうち、node.children に無いものがあれば「展開」
            untried = [a for a in legal if a not in node.children]

            # 「availability」を全合法手分だけ +1 する (親ノードで記録)
            # = この選択肢がこの iteration で出現した
            for a in legal:
                if a in node.children:
                    node.children[a].availability += 1

            if untried:
                # 展開: 未訪問の手から1つ選ぶ
                action = self.rng.choice(untried)
                det_game.step(action)
                child = ISMCTSNode(
                    parent=node,
                    incoming_action=action,
                    player_to_move=det_game.current_player() if not det_game.is_terminal() else -1,
                )
                # 新しい子は今回初出現なので availability=1
                child.availability = 1
                node.children[action] = child
                node = child
                path.append(node)
                break  # 展開後はロールアウトへ
            else:
                # すべての合法手が展開済み → UCB1 で1つ選択
                action = self._ucb_select(node, legal)
                det_game.step(action)
                node = node.children[action]
                path.append(node)

        # -------- Rollout (ランダムプレイアウト) --------
        while not det_game.is_terminal():
            legal = det_game.get_legal_actions()
            action = self.rng.choice(legal)
            det_game.step(action)

        # -------- Backpropagation --------
        reward = compute_reward_for(det_game, root_player)
        for n in path:
            n.visits += 1
            # total_reward は「そのノードに到達した後の結果」を貯めるが、
            # SO-ISMCTS では全ノードで root_player の報酬を使ってよい
            # (他プレイヤーの手番でも、root_player 視点の勝率を学ぶ)
            n.total_reward += reward

    def _ucb_select(self, node: ISMCTSNode, legal_actions: list[tuple]) -> tuple:
        """UCB1 で合法手の中から1つ選ぶ。"""
        best_action = None
        best_score = -float("inf")
        log_avail_parent = math.log(max(1, sum(
            node.children[a].availability for a in legal_actions
        )))
        # 分母に使うのは「この選択肢が出現した availability」
        for a in legal_actions:
            child = node.children[a]
            if child.visits == 0:
                # 普通はexpansionで拾うのでここには来ないが保険
                return a
            exploit = child.total_reward / child.visits
            explore = self.c_uct * math.sqrt(log_avail_parent / child.availability)
            score = exploit + explore
            if score > best_score:
                best_score = score
                best_action = a
        return best_action


# ============================================================
# 単体テスト的な動作確認
# ============================================================

if __name__ == "__main__":
    import time

    # ISMCTS を1手だけ動かしてみる
    game = StartupsGame(seed=42)
    agent = ISMCTS(iterations=500, rng=random.Random(0))

    print("=== 初手の探索 (500 iterations) ===")
    print(game.render())

    start = time.time()
    action = agent.search(game, root_player=0)
    elapsed = time.time() - start

    print(f"\nISMCTS が選んだ手: {action}")
    print(f"所要時間: {elapsed:.2f}秒")
    print(f"ルート直下のノード数: {len(game.get_legal_actions())}")
