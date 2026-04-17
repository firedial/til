"""
スタータップス(Startups) - ゲームエンジン
3人プレイ、フルルール版

AI学習用に設計されており、以下を提供:
  - 状態管理(完全情報)
  - 観測取得(各プレイヤー視点の不完全情報)
  - 合法手列挙
  - 行動適用・勝敗判定
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import random


# ============================================================
# 定数定義
# ============================================================

NUM_PLAYERS = 3
NUM_COMPANIES = 6
COMPANY_SIZES = [5, 6, 7, 8, 9, 10]  # 各企業のカード枚数 (index 0..5)
TOTAL_CARDS = sum(COMPANY_SIZES)       # 45
INITIAL_COINS = 10
HAND_SIZE = 3
REMOVED_CARDS = 5                      # ゲーム開始時に裏向きで除外する枚数


# ============================================================
# 行動(Action)の定義
# ============================================================
# 行動は (種類, パラメータ) のタプルで表現。
# 行動種類は3つ:
#   "draw_deck"           : 山札から1枚引く(マーケットが空、
#                            あるいは独禁チップ効果で支払い免除、
#                            あるいはマーケットに全カードにコインを置いて引く)
#   "draw_market"         : マーケットから特定のカード(会社index)を取る
#   "play"                : 手札の1枚を投資 or 放流
#
# 正確なタプル表現:
#   ("draw_deck",)                                 # ドロー(フェーズ1)
#   ("draw_market", company_idx)                   # マーケットから取る(フェーズ1)
#   ("play_invest", company_idx, from_market_flag) # 投資(フェーズ2)
#   ("play_discard", company_idx)                  # 放流(フェーズ2、市場由来NG)

Action = tuple


# ============================================================
# ゲーム状態
# ============================================================

@dataclass
class PlayerState:
    # 手札は会社インデックスのリスト(単純)
    hand: list[int] = field(default_factory=list)
    # 自分の場に出した投資カード(会社ごとの枚数)
    invested: list[int] = field(default_factory=lambda: [0] * NUM_COMPANIES)
    coins: int = INITIAL_COINS
    # 保持している独禁チップ(会社ごとに 0/1)
    antitrust: list[int] = field(default_factory=lambda: [0] * NUM_COMPANIES)


@dataclass
class GameState:
    deck: list[int] = field(default_factory=list)           # 山札(会社インデックスの列)
    market: list[int] = field(default_factory=list)          # マーケットの捨て札(会社インデックス)
    market_coins: list[int] = field(default_factory=list)    # 各マーケットカードに乗っているコイン数
    players: list[PlayerState] = field(default_factory=list)
    current_player: int = 0
    # 独禁チップの現所有者(会社ごと)。-1なら誰も保持していない。
    antitrust_owner: list[int] = field(default_factory=lambda: [-1] * NUM_COMPANIES)
    # 手番のフェーズ: "draw" or "play"
    phase: str = "draw"
    # この手番でマーケットから取った企業(ドローフェーズでマーケットから引いた時に設定)
    # プレイフェーズで「その企業と同じカード」を放流できない制約に使う
    # None なら制約なし(山札から引いた手番、またはプレイフェーズ終了後)
    market_locked_company: Optional[int] = None
    # 終了フラグ
    terminal: bool = False
    # rng
    rng: random.Random = field(default_factory=random.Random)


# ============================================================
# ゲームエンジン本体
# ============================================================

class StartupsGame:
    """スタータップスのゲームエンジン。

    使い方:
        game = StartupsGame(seed=42)
        while not game.is_terminal():
            player = game.current_player()
            actions = game.get_legal_actions()
            action = actions[0]  # なんらかの方針で選ぶ
            game.step(action)
        rewards = game.get_rewards()
    """

    def __init__(self, seed: Optional[int] = None):
        self.state = GameState()
        self.state.rng = random.Random(seed)
        self._setup()

    # --------------------------------------------------------
    # 初期化
    # --------------------------------------------------------
    def _setup(self):
        s = self.state
        # カード生成: 会社0は5枚、会社1は6枚...
        all_cards: list[int] = []
        for c_idx, size in enumerate(COMPANY_SIZES):
            all_cards.extend([c_idx] * size)
        s.rng.shuffle(all_cards)

        # 5枚を除外(ゲームから取り除く)
        removed = all_cards[:REMOVED_CARDS]
        remaining = all_cards[REMOVED_CARDS:]

        # プレイヤー初期化 + 手札配布
        s.players = [PlayerState() for _ in range(NUM_PLAYERS)]
        idx = 0
        for p in s.players:
            for _ in range(HAND_SIZE):
                p.hand.append(remaining[idx])
                idx += 1
        # 残りが山札
        s.deck = remaining[idx:]
        s.market = []
        s.market_coins = []
        s.current_player = 0
        s.phase = "draw"
        s.market_locked_company = None
        s.terminal = False

    # --------------------------------------------------------
    # 状態クエリ
    # --------------------------------------------------------
    def current_player(self) -> int:
        return self.state.current_player

    def is_terminal(self) -> bool:
        return self.state.terminal

    def get_phase(self) -> str:
        return self.state.phase

    # --------------------------------------------------------
    # 合法手の列挙
    # --------------------------------------------------------
    def get_legal_actions(self) -> list[Action]:
        """現プレイヤー・現フェーズでの合法行動リストを返す。"""
        s = self.state
        p = s.players[s.current_player]
        actions: list[Action] = []

        if s.phase == "draw":
            # 山札から引く選択肢
            if len(s.deck) > 0:
                if len(s.market) == 0:
                    # マーケット空 → 無条件で山札から引ける
                    actions.append(("draw_deck",))
                else:
                    # マーケットにカードがある
                    # 独禁チップで持ってる企業がマーケットにあるなら支払い免除で山札から引ける
                    has_free_draw = any(
                        p.antitrust[s.market[i]] == 1 for i in range(len(s.market))
                    )
                    if has_free_draw:
                        actions.append(("draw_deck",))
                    else:
                        # 山札から引くにはマーケット全カードにコイン1枚ずつ置く必要
                        if p.coins >= len(s.market):
                            actions.append(("draw_deck",))

            # マーケットから取る選択肢(市場にある各カード、ただし独禁保有企業は取れない)
            seen = set()
            for i, c_idx in enumerate(s.market):
                if c_idx in seen:
                    continue
                seen.add(c_idx)
                if p.antitrust[c_idx] == 1:
                    continue  # 独禁保有企業は取れない
                actions.append(("draw_market", c_idx))

        elif s.phase == "play":
            # 投資 or 放流
            for i, c_idx in enumerate(p.hand):
                # 投資は常に可能(手札位置iのカードを投資)
                actions.append(("play_invest", i))
                # 放流制約: この手番でマーケットから取った企業と同じ数字(=同じ企業)は放流禁止
                if s.market_locked_company is None or c_idx != s.market_locked_company:
                    actions.append(("play_discard", i))
            # 重複除去
            actions = list(dict.fromkeys(actions))

        return actions

    # --------------------------------------------------------
    # 行動適用
    # --------------------------------------------------------
    def step(self, action: Action):
        """行動を適用して状態を進める。"""
        s = self.state
        if s.terminal:
            raise RuntimeError("Game is already terminal.")

        if s.phase == "draw":
            self._apply_draw(action)
            s.phase = "play"
        elif s.phase == "play":
            self._apply_play(action)
            # 次のプレイヤーへ
            s.current_player = (s.current_player + 1) % NUM_PLAYERS
            s.phase = "draw"
            # 終了判定
            if len(s.deck) == 0:
                self._resolve_endgame()

    def _apply_draw(self, action: Action):
        """ドローフェーズの行動を適用。"""
        s = self.state
        p = s.players[s.current_player]
        kind = action[0]

        # 手番の最初にロックをリセット(安全のため)
        s.market_locked_company = None

        if kind == "draw_deck":
            # マーケットにカードがあり、独禁チップによる免除がない場合、コイン支払い
            if len(s.market) > 0:
                has_free = any(p.antitrust[s.market[i]] == 1 for i in range(len(s.market)))
                if not has_free:
                    # 各マーケットカードにコイン1枚ずつ置く
                    for i in range(len(s.market)):
                        s.market_coins[i] += 1
                        p.coins -= 1
            # 山札から1枚引く
            card = s.deck.pop(0)
            p.hand.append(card)

        elif kind == "draw_market":
            target_company = action[1]
            # 先頭から同じ会社のカードを取る
            for i, c_idx in enumerate(s.market):
                if c_idx == target_company:
                    s.market.pop(i)
                    # そのカードに乗っていたコインを獲得
                    coins_on_card = s.market_coins.pop(i)
                    p.coins += coins_on_card
                    # 手札に追加
                    p.hand.append(c_idx)
                    # 同じ企業の放流を禁止
                    s.market_locked_company = c_idx
                    break
        else:
            raise ValueError(f"Invalid draw action: {action}")

    def _apply_play(self, action: Action):
        """プレイフェーズの行動を適用。"""
        s = self.state
        p = s.players[s.current_player]
        kind = action[0]
        hand_idx = action[1]
        c_idx = p.hand[hand_idx]

        if kind == "play_invest":
            # 自分の場に投資
            # 新規参入(0→1)の場合、誰も独禁チップを持っていなければ自分が獲得
            is_new_entry = (p.invested[c_idx] == 0)
            p.invested[c_idx] += 1
            p.hand.pop(hand_idx)

            if is_new_entry and s.antitrust_owner[c_idx] == -1:
                # 最初の投資者 → 独禁チップ獲得
                s.antitrust_owner[c_idx] = s.current_player
                p.antitrust[c_idx] = 1
            else:
                # 既に誰かが保有中。最大投資者に移動する可能性
                self._update_antitrust(c_idx)

        elif kind == "play_discard":
            # マーケットに放流(market_locked_companyと同じ企業は不可)
            if s.market_locked_company is not None and c_idx == s.market_locked_company:
                raise ValueError(
                    f"Cannot discard company {c_idx}: locked by market draw this turn"
                )
            s.market.append(c_idx)
            s.market_coins.append(0)
            p.hand.pop(hand_idx)
        else:
            raise ValueError(f"Invalid play action: {action}")

        # プレイフェーズが終わるのでロック解除
        s.market_locked_company = None

    def _update_antitrust(self, c_idx: int):
        """企業 c_idx の投資状況を見て独禁チップの所有者を更新。"""
        s = self.state
        # 全プレイヤーの投資枚数をチェック
        counts = [p.invested[c_idx] for p in s.players]
        max_count = max(counts)
        if max_count == 0:
            return
        # 最大投資者(同数なら複数いる可能性あり)
        top_players = [i for i, c in enumerate(counts) if c == max_count]

        current_owner = s.antitrust_owner[c_idx]

        if len(top_players) == 1:
            # 単独トップ → その人が保有
            new_owner = top_players[0]
            if new_owner != current_owner:
                if current_owner != -1:
                    s.players[current_owner].antitrust[c_idx] = 0
                s.antitrust_owner[c_idx] = new_owner
                s.players[new_owner].antitrust[c_idx] = 1
        else:
            # 同数トップ複数 → 現所有者が top_players にいれば保持、そうでなければ空席にする
            # (公式ルールでは前の所有者が保持するケースが自然)
            if current_owner in top_players:
                pass  # 現状維持
            else:
                # 現所有者が最大でない → チップは宙に浮く
                # ルール上はその状態があまりない(次の投資で決着する)が、
                # ここでは「誰かが単独トップになるまで現所有者のまま」とする実装もある。
                # 厳密には公式ルールで「同点の場合はチップが置かれない」になる事もあるが、
                # 実装簡略化のため現所有者保持を採用する。
                pass

    # --------------------------------------------------------
    # 終局処理
    # --------------------------------------------------------
    def _resolve_endgame(self):
        """山札が尽きたとき: 残り手札を全て投資 → 得点計算。"""
        s = self.state
        # 残り手札を全員投資(強制)
        for pid, p in enumerate(s.players):
            for c_idx in p.hand:
                p.invested[c_idx] += 1
            p.hand = []
        # 最終的な独禁チップ所有者を全企業で更新
        for c_idx in range(NUM_COMPANIES):
            self._update_antitrust(c_idx)

        # 得点計算(終局時):
        # 各企業ごと、単独最大投資者が、その企業に投資している "他の各プレイヤー"
        # からコインを徴収する。
        #
        # 裏返しコインルール:
        #   支払う側 → N枚のコインを手放す(= coins -= N)
        #   受け取る側 → そのN枚を「裏面=3コイン価値」で受け取る(= coins += 3*N)
        # これによりコインの総量はゲーム終了時に増える。
        #
        # Nの決め方: 徴収される側の投資枚数(2位以下は自分の投資枚数ぶんを支払う)
        COIN_FLIP_VALUE = 3
        for c_idx in range(NUM_COMPANIES):
            counts = [p.invested[c_idx] for p in s.players]
            max_count = max(counts)
            if max_count == 0:
                continue
            top = [i for i, c in enumerate(counts) if c == max_count]
            if len(top) != 1:
                continue  # 同数トップは得点なし
            winner = top[0]
            for other_pid, other_p in enumerate(s.players):
                if other_pid == winner:
                    continue
                pay = other_p.invested[c_idx]
                if pay > 0:
                    other_p.coins -= pay
                    s.players[winner].coins += pay * COIN_FLIP_VALUE

        s.terminal = True

    # --------------------------------------------------------
    # 報酬(勝敗)
    # --------------------------------------------------------
    def get_rewards(self) -> list[float]:
        """各プレイヤーの報酬を返す。
        シンプルには「最終コイン数」を使う。
        勝敗ベースにしたければ、最大コイン者に+1、他に0等に変更可能。
        """
        assert self.state.terminal
        return [float(p.coins) for p in self.state.players]

    def get_winner(self) -> Optional[int]:
        """単独勝者がいればそのID、引き分けならNone。"""
        assert self.state.terminal
        coins = [p.coins for p in self.state.players]
        m = max(coins)
        top = [i for i, c in enumerate(coins) if c == m]
        if len(top) == 1:
            return top[0]
        return None

    # --------------------------------------------------------
    # 観測(不完全情報)
    # --------------------------------------------------------
    def get_observation(self, player_id: int) -> dict:
        """プレイヤー player_id から見える情報だけを返す。

        見えるもの:
          - 自分の手札
          - 自分のコイン
          - 自分の投資状況・独禁チップ保有
          - 全プレイヤーの投資状況・独禁チップ保有(公開情報)
          - 全プレイヤーのコイン(公開情報)
          - マーケット・各カード上のコイン
          - 山札の残り枚数(中身は見えない)
          - 現プレイヤー・フェーズ
        見えないもの:
          - 他プレイヤーの手札
          - 山札の中身
          - 除外された5枚
        """
        s = self.state
        my = s.players[player_id]
        return {
            "player_id": player_id,
            "my_hand": list(my.hand),
            "my_coins": my.coins,
            "my_invested": list(my.invested),
            "my_antitrust": list(my.antitrust),
            "all_invested": [list(p.invested) for p in s.players],
            "all_antitrust": [list(p.antitrust) for p in s.players],
            "all_coins": [p.coins for p in s.players],
            "all_hand_sizes": [len(p.hand) for p in s.players],
            "market": list(s.market),
            "market_coins": list(s.market_coins),
            "deck_size": len(s.deck),
            "antitrust_owner": list(s.antitrust_owner),
            "current_player": s.current_player,
            "phase": s.phase,
            "market_locked_company": s.market_locked_company,
        }

    # --------------------------------------------------------
    # デバッグ表示
    # --------------------------------------------------------
    def render(self) -> str:
        s = self.state
        lines = []
        lines.append(f"=== Turn: Player {s.current_player}, Phase: {s.phase} ===")
        lines.append(f"Deck: {len(s.deck)} cards remaining")
        lines.append(f"Market: {s.market} (coins on each: {s.market_coins})")
        lines.append(f"Antitrust owners: {s.antitrust_owner}")
        for i, p in enumerate(s.players):
            marker = " <-" if i == s.current_player else ""
            lines.append(
                f"  P{i}: coins={p.coins}, invested={p.invested}, "
                f"antitrust={p.antitrust}, hand_size={len(p.hand)}{marker}"
            )
        if s.terminal:
            lines.append(f"[TERMINAL] coins = {[p.coins for p in s.players]}")
            w = self.get_winner()
            lines.append(f"  Winner: {'P'+str(w) if w is not None else 'Draw'}")
        return "\n".join(lines)
