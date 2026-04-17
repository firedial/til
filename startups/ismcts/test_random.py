"""
スタータップスのランダムAI対戦テスト。
ゲームエンジンの動作確認 + ベースラインAI。
"""

from startups import StartupsGame, NUM_PLAYERS
import random
from collections import Counter


def random_policy(game: StartupsGame, rng: random.Random) -> tuple:
    """合法手からランダムに1つ選ぶ。"""
    actions = game.get_legal_actions()
    return rng.choice(actions)


def greedy_policy(game: StartupsGame, rng: random.Random) -> tuple:
    """ちょっとだけ賢いベースライン:
      - 投資できるなら投資(独禁チップを狙いに行く)
      - そうでなければ山札から引く
      - それもダメなら市場からランダム
    """
    actions = game.get_legal_actions()
    # 投資行動を優先
    invests = [a for a in actions if a[0] == "play_invest"]
    if invests:
        return rng.choice(invests)
    # 山札から引くのを優先
    draws = [a for a in actions if a[0] == "draw_deck"]
    if draws:
        return draws[0]
    return rng.choice(actions)


def play_one_game(policies: list, seed: int, verbose: bool = False) -> list[float]:
    """1ゲーム実行して各プレイヤーの最終コインを返す。"""
    game = StartupsGame(seed=seed)
    rng = random.Random(seed + 1000)
    step_count = 0
    max_steps = 1000  # 無限ループ防止

    while not game.is_terminal() and step_count < max_steps:
        pid = game.current_player()
        action = policies[pid](game, rng)
        if verbose:
            print(game.render())
            print(f"  Player {pid} chose: {action}")
        game.step(action)
        step_count += 1

    if verbose:
        print("\n=== GAME END ===")
        print(game.render())

    if not game.is_terminal():
        raise RuntimeError(f"Game didn't terminate in {max_steps} steps")

    return game.get_rewards()


def run_tournament(policies: list, num_games: int, base_seed: int = 0):
    """ num_games ゲーム回して統計を出す。"""
    total_coins = [0.0] * NUM_PLAYERS
    wins = Counter()
    draws = 0

    for g in range(num_games):
        seed = base_seed + g
        rewards = play_one_game(policies, seed)
        for i, r in enumerate(rewards):
            total_coins[i] += r
        m = max(rewards)
        top = [i for i, r in enumerate(rewards) if r == m]
        if len(top) == 1:
            wins[top[0]] += 1
        else:
            draws += 1

    print(f"\n=== Tournament result ({num_games} games) ===")
    for i in range(NUM_PLAYERS):
        avg = total_coins[i] / num_games
        winrate = wins[i] / num_games * 100
        print(f"  P{i}: avg_coins={avg:.2f}, wins={wins[i]} ({winrate:.1f}%)")
    print(f"  Draws: {draws} ({draws/num_games*100:.1f}%)")


if __name__ == "__main__":
    # 1. まず1ゲームだけ詳細表示で動かして挙動確認
    print("===== Single game (verbose) =====")
    play_one_game([random_policy] * 3, seed=42, verbose=True)

    # 2. ランダム同士で100ゲーム
    print("\n\n===== Random vs Random vs Random (100 games) =====")
    run_tournament([random_policy] * 3, num_games=100)

    # 3. P0だけgreedy、他はランダム
    print("\n\n===== Greedy(P0) vs Random(P1) vs Random(P2) (500 games) =====")
    run_tournament(
        [greedy_policy, random_policy, random_policy],
        num_games=500,
    )
