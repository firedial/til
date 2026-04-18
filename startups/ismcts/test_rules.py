"""
スタータップスのルール実装を検証する単体テスト。
主に訂正された「同企業放流禁止ルール」を確認。
"""

from startups import StartupsGame, GameState, PlayerState


def test_market_lock_same_company():
    """マーケットから会社Xを取ったら、手札の同じ会社Xのカードは放流できないことを確認。"""
    game = StartupsGame(seed=0)
    s = game.state

    # シナリオを手動でセットアップ:
    # P0 の手札に company 2 を複数枚持たせ、マーケットに company 2 を入れておく
    s.players[0].hand = [2, 2, 5]  # company 2 が2枚、company 5 が1枚
    s.players[0].coins = 10
    s.market = [2]  # マーケットに company 2
    s.market_coins = [0]
    s.current_player = 0
    s.phase = "draw"
    s.market_locked_company = None
    s.deck = [0, 1, 3, 4]  # 適当に

    # ドローフェーズ: マーケットから company 2 を取る
    game.step(("draw_market", 2))

    # この時点で:
    # - 手札に company 2 が3枚になっているはず
    # - market_locked_company = 2 になっているはず
    assert s.players[0].hand.count(2) == 3, f"手札: {s.players[0].hand}"
    assert s.market_locked_company == 2, f"lock: {s.market_locked_company}"
    assert s.phase == "play"

    # プレイフェーズの合法手を取得
    legal = game.get_legal_actions()
    print(f"合法手: {legal}")

    # 期待: company 2 の放流(play_discard)は禁止、company 5 の放流はOK
    # company 2 の投資(play_invest)はOK
    discards = [a for a in legal if a[0] == "play_discard"]
    for a in discards:
        hand_idx = a[1]
        c = s.players[0].hand[hand_idx]
        assert c != 2, f"company 2 の放流が合法手に入っている! hand_idx={hand_idx}, hand={s.players[0].hand}"

    # company 5 (index 2 の位置) の放流は合法
    assert ("play_discard", 2) in legal, f"company 5 の放流が合法手にない"

    # company 2 の投資は合法
    assert ("play_invest", 0) in legal
    assert ("play_invest", 1) in legal

    print("✅ test_market_lock_same_company: PASS")


def test_market_lock_reset_next_turn():
    """ロックは手番終了で解除されることを確認。"""
    game = StartupsGame(seed=1)
    s = game.state
    s.players[0].hand = [2, 2, 5]
    s.players[0].coins = 10
    s.market = [2]
    s.market_coins = [0]
    s.current_player = 0
    s.phase = "draw"
    s.market_locked_company = None
    s.deck = [0, 1, 3, 4]

    game.step(("draw_market", 2))  # P0 がマーケットから company 2 を取る
    assert s.market_locked_company == 2

    # P0 がプレイ(例: company 5 を放流)
    # hand: [2, 2, 5, 2] (先頭3枚+マーケットから取った1枚) → play_discard の hand_idx=2 は 5
    print(f"プレイ前の手札: {s.players[0].hand}")
    idx5 = s.players[0].hand.index(5)
    game.step(("play_discard", idx5))

    # プレイ後はロック解除されているはず
    assert s.market_locked_company is None, f"ロックが残っている: {s.market_locked_company}"
    # 次はP1のターン
    assert s.current_player == 1

    print("✅ test_market_lock_reset_next_turn: PASS")


def test_deck_draw_does_not_lock():
    """山札から引いた場合はロックがかからないことを確認。"""
    game = StartupsGame(seed=2)
    s = game.state
    s.players[0].hand = [2, 2, 5]
    s.market = []
    s.market_coins = []
    s.current_player = 0
    s.phase = "draw"
    s.market_locked_company = None
    s.deck = [3, 4]  # 山札に適当なカード

    game.step(("draw_deck",))
    assert s.market_locked_company is None
    assert s.phase == "play"

    # 全部のカードが放流可能
    legal = game.get_legal_actions()
    discards = [a for a in legal if a[0] == "play_discard"]
    # 手札は4枚、重複除去後の company 2 と company 5 と引いたカード(3 or 4)で3種類 → 3つ以上の放流
    discard_companies = {s.players[0].hand[a[1]] for a in discards}
    assert 2 in discard_companies
    assert 5 in discard_companies

    print("✅ test_deck_draw_does_not_lock: PASS")


def test_antitrust_blocks_market_pick():
    """独禁チップ保有者はその企業をマーケットから取れないことを確認。"""
    game = StartupsGame(seed=3)
    s = game.state
    s.players[0].hand = [0, 1, 2]
    s.players[0].coins = 10
    s.players[0].antitrust[4] = 1  # company 4 の独禁を保有
    s.antitrust_owner[4] = 0
    s.market = [4, 5]
    s.market_coins = [0, 0]
    s.current_player = 0
    s.phase = "draw"
    s.deck = [0, 1]

    legal = game.get_legal_actions()
    # company 4 は独禁持ち → 取れない
    assert ("draw_market", 4) not in legal
    # company 5 は取れる
    assert ("draw_market", 5) in legal

    print("✅ test_antitrust_blocks_market_pick: PASS")


def test_antitrust_free_draw():
    """独禁保有企業のカードにだけコインを置かない(部分免除)。"""
    game = StartupsGame(seed=4)
    s = game.state
    s.players[0].hand = [0, 1, 2]
    initial_coins = 10
    s.players[0].coins = initial_coins
    s.players[0].antitrust[4] = 1  # company 4 の独禁
    s.antitrust_owner[4] = 0
    s.market = [4, 5]       # company4(独禁あり), company5(独禁なし)
    s.market_coins = [0, 0]
    s.current_player = 0
    s.phase = "draw"
    s.deck = [0, 1]

    game.step(("draw_deck",))
    # company 4 は免除、company 5 にだけコイン1枚置く → 1コイン減
    assert s.players[0].coins == initial_coins - 1, \
        f"独禁企業は免除で1枚だけ減るはず: {s.players[0].coins}"
    # company 4 のカードにはコイン0、company 5 のカードにはコイン1
    assert s.market_coins[0] == 0, f"独禁企業にコインが乗った: {s.market_coins}"
    assert s.market_coins[1] == 1, f"非独禁企業にコインが乗っていない: {s.market_coins}"

    print("✅ test_antitrust_free_draw: PASS")


def test_antitrust_all_free():
    """マーケットの全カードが独禁企業なら、コイン0枚で山札から引ける。"""
    game = StartupsGame(seed=7)
    s = game.state
    s.players[0].hand = [0, 1, 2]
    s.players[0].coins = 10
    s.players[0].antitrust[3] = 1
    s.players[0].antitrust[4] = 1
    s.antitrust_owner[3] = 0
    s.antitrust_owner[4] = 0
    s.market = [3, 4]
    s.market_coins = [0, 0]
    s.current_player = 0
    s.phase = "draw"
    s.deck = [0, 1]

    game.step(("draw_deck",))
    assert s.players[0].coins == 10, f"全免除なのにコインが減った: {s.players[0].coins}"
    assert all(c == 0 for c in s.market_coins), f"コインが乗った: {s.market_coins}"

    print("✅ test_antitrust_all_free: PASS")


def test_scoring():
    """得点計算: 単独トップが他プレイヤーから投資枚数ぶんのコインを徴収(裏返し=3倍で受取)。"""
    game = StartupsGame(seed=5)
    s = game.state
    s.players[0].invested = [3, 0, 0, 0, 0, 0]
    s.players[1].invested = [1, 0, 0, 0, 0, 0]
    s.players[2].invested = [2, 0, 0, 0, 0, 0]
    s.players[0].hand = []
    s.players[1].hand = []
    s.players[2].hand = []
    s.players[0].coins = 10
    s.players[1].coins = 10
    s.players[2].coins = 10
    s.deck = []
    s.market = []
    s.market_coins = []
    s.phase = "play"
    s.current_player = 0
    game._resolve_endgame()

    # P0: 10 + 1*3 + 2*3 = 19
    # P1: 10 - 1 = 9
    # P2: 10 - 2 = 8
    assert s.players[0].coins == 19, f"P0: {s.players[0].coins}"
    assert s.players[1].coins == 9, f"P1: {s.players[1].coins}"
    assert s.players[2].coins == 8, f"P2: {s.players[2].coins}"

    # ポイント制: P0=1位→2点, P1=2位→1点, P2=3位→-1点
    rewards = game.get_rewards()
    assert rewards == [2, 1, -1], f"rewards: {rewards}"

    print("✅ test_scoring: PASS")


def test_scoring_tie_no_payment():
    """単独トップがいない(同数トップ)場合は誰も徴収しない。"""
    game = StartupsGame(seed=6)
    s = game.state
    s.players[0].invested = [2, 0, 0, 0, 0, 0]
    s.players[1].invested = [2, 0, 0, 0, 0, 0]
    s.players[2].invested = [1, 0, 0, 0, 0, 0]
    for p in s.players:
        p.hand = []
        p.coins = 10
    s.deck = []
    s.market = []
    s.market_coins = []

    game._resolve_endgame()

    for i, p in enumerate(s.players):
        assert p.coins == 10, f"P{i} のコインが変わった: {p.coins}"

    print("✅ test_scoring_tie_no_payment: PASS")


def test_tiebreak_larger_company():
    """コイン同点時、より大きい企業で単独最大投資している方が上位。"""
    game = StartupsGame(seed=8)
    s = game.state
    # 全員10コインで同点にする
    # P0: company 0 (小さい企業) で単独トップ
    # P1: company 5 (大きい企業) で単独トップ
    # P2: 何も単独トップなし
    s.players[0].invested = [3, 0, 0, 0, 0, 0]
    s.players[1].invested = [0, 0, 0, 0, 0, 3]
    s.players[2].invested = [0, 0, 0, 0, 0, 0]
    for p in s.players:
        p.hand = []
        p.coins = 10  # 全員同点
    s.deck = []
    s.market = []
    s.market_coins = []
    s.turn_order = [0, 1, 2]
    game._resolve_endgame()

    # コインは変わらない(単独トップがいるが他者の投資枚数0なので徴収0)
    ranking = game.get_ranking()
    # P1 が上位(大きい企業 company 5 で単独トップ) → 1位
    # P0 が次(company 0 で単独トップ) → 2位
    # P2 が最下位 → 3位
    assert ranking[1] == 1, f"P1 should be 1st, got {ranking}"
    assert ranking[0] == 2, f"P0 should be 2nd, got {ranking}"
    assert ranking[2] == 3, f"P2 should be 3rd, got {ranking}"

    print("✅ test_tiebreak_larger_company: PASS")


def test_tiebreak_late_start():
    """企業タイブレークでも決まらない場合、初手が遅い方が上位。"""
    game = StartupsGame(seed=9)
    s = game.state
    # 全員同コイン、誰も単独トップなし
    for p in s.players:
        p.invested = [0, 0, 0, 0, 0, 0]
        p.hand = []
        p.coins = 10
    s.deck = []
    s.market = []
    s.market_coins = []
    s.turn_order = [0, 1, 2]  # P0先手, P2後手
    game._resolve_endgame()

    ranking = game.get_ranking()
    # 初手が遅い方が上位 → P2(turn_order=2) > P1(1) > P0(0)
    assert ranking[2] == 1, f"P2 should be 1st, got {ranking}"
    assert ranking[1] == 2, f"P1 should be 2nd, got {ranking}"
    assert ranking[0] == 3, f"P0 should be 3rd, got {ranking}"

    print("✅ test_tiebreak_late_start: PASS")


def test_rewards_points():
    """get_rewards が int の [2, 1, -1] を返すことを確認。"""
    game = StartupsGame(seed=10)
    s = game.state
    s.players[0].invested = [5, 0, 0, 0, 0, 0]
    s.players[1].invested = [0, 3, 0, 0, 0, 0]
    s.players[2].invested = [0, 0, 0, 0, 0, 0]
    for p in s.players:
        p.hand = []
        p.coins = 10
    s.deck = []
    s.market = []
    s.market_coins = []
    game._resolve_endgame()

    rewards = game.get_rewards()
    assert all(isinstance(r, int) for r in rewards), f"rewards should be int: {rewards}"
    assert sorted(rewards, reverse=True) == [2, 1, -1], f"rewards: {rewards}"
    # get_winner は必ずだれかを返す
    w = game.get_winner()
    assert w is not None, "winner should not be None with tiebreak"

    print("✅ test_rewards_points: PASS")


if __name__ == "__main__":
    test_market_lock_same_company()
    test_market_lock_reset_next_turn()
    test_deck_draw_does_not_lock()
    test_antitrust_blocks_market_pick()
    test_antitrust_free_draw()
    test_antitrust_all_free()
    test_scoring()
    test_scoring_tie_no_payment()
    test_tiebreak_larger_company()
    test_tiebreak_late_start()
    test_rewards_points()
    print("\n🎉 全テストPASS")
