import random
import math
import concurrent.futures


def isWin(sigmaProb: float, p1: float, p2: float) -> int:
    u = random.uniform(0.0, 1.0)
    b = sigmaProb / (1 - sigmaProb)
    p = 1 / (b ** (p2 - p1) + 1)
    return 1 if u < p else -1


def getRank(players: list[float | int]) -> list[int]:
    indexed = sorted(enumerate(players), key=lambda x: x[1], reverse=True)
    ranks = [0] * len(players)
    for rank, (original_idx, _) in enumerate(indexed, 1):
        ranks[original_idx] = rank
    return ranks


def roundRobinTournament(sigmaProb: float, players: list[float | int]) -> list[int]:
    playerCount = len(players)
    results = [[0] * playerCount for _ in range(playerCount)]

    for i in range(playerCount):
        for j in range(i + 1, playerCount):
            r = isWin(sigmaProb, players[i], players[j])
            results[i][j] = r
            results[j][i] = -r

    winCounts = [sum(results[i]) for i in range(playerCount)]
    ranking = sorted(range(playerCount), key=lambda i: (-winCounts[i], i))
    return ranking[:4]


def tournament(sigmaProb: float, players: list[float | int]) -> list[int]:
    def match(a, b):
        r = isWin(sigmaProb, a[1], b[1])
        return (a, b) if r == 1 else (b, a)  # (勝者, 敗者)

    current = list(enumerate(players))

    while len(current) > 4:
        current = [match(current[i], current[i + len(current) // 2])[0]
                   for i in range(len(current) // 2)]

    winner1, loser1 = match(current[0], current[1])
    winner2, loser2 = match(current[2], current[3])
    first, second = match(winner1, winner2)
    third, fourth = match(loser1, loser2)

    return [first[0], second[0], third[0], fourth[0]]


def swissTournament(sigmaProb: float, players: list[float | int]) -> list[int]:
    playerCount = len(players)
    indexed_players = list(enumerate(players))
    # 各プレイヤーの勝ち負け履歴 例: [1, -1, 1] = 勝ち・負け・勝ち
    history = {i: [] for i in range(playerCount)}

    for _ in range(int(math.log2(playerCount))):
        # 履歴が同じグループにまとめる
        groups = {}
        for player in indexed_players:
            key = tuple(history[player[0]])
            groups.setdefault(key, []).append(player)

        pairs = []
        for group in groups.values():
            # グループ内でペアリング
            for i in range(0, len(group), 2):
                pairs.append((group[i], group[i + 1]))

        for a, b in pairs:
            if isWin(sigmaProb, a[1], b[1]) == 1:
                history[a[0]].append(1)
                history[b[0]].append(-1)
            else:
                history[a[0]].append(-1)
                history[b[0]].append(1)

    ranking = sorted(range(playerCount), key=lambda i: (-sum(history[i]), i))
    return ranking[:4]


def doubleEliminationTournament(sigmaProb: float, players: list[float | int]) -> list[int]:
    indexed_players = list(enumerate(players))

    def match(a, b):
        r = isWin(sigmaProb, a[1], b[1])
        return (a, b) if r == 1 else (b, a)  # (勝者, 敗者)

    winners_bracket = indexed_players.copy()
    losers_bracket = []

    # 勝者側・敗者側を交互に進める
    while len(winners_bracket) > 2:
        # 勝者側1ラウンド
        next_winners = []
        new_losers = []
        for i in range(len(winners_bracket) // 2):
            winner, loser = match(winners_bracket[i], winners_bracket[i + len(winners_bracket) // 2])
            next_winners.append(winner)
            new_losers.append(loser)
        winners_bracket = next_winners

        # 敗者側：既存の敗者同士で1ラウンド戦ってから新規敗者と合流
        if losers_bracket:
            next_losers = []
            for i in range(len(losers_bracket) // 2):
                winner, _ = match(losers_bracket[i], losers_bracket[i + len(losers_bracket) // 2])
                next_losers.append(winner)
            losers_bracket = next_losers

        losers_bracket.extend(new_losers)

    # 敗者側決勝（4位はここの敗者）
    losers_finalist, fourth = match(losers_bracket[0], losers_bracket[1])

    # 勝者側決勝
    winners_finalist, winners_loser = match(winners_bracket[0], winners_bracket[1])
    losers_bracket.append(winners_loser)

    # 負けたら3位、勝ったら大決勝
    second_candidate, third = match(winners_loser, losers_finalist)

    # 大決勝
    final_winner, final_loser = match(winners_finalist, second_candidate)
    if final_winner == second_candidate:
        # 敗者側が勝った場合、グランドファイナル
        first, second = match(winners_finalist, second_candidate)
    else:
        first = final_winner
        second = second_candidate

    return [first[0], second[0], third[0], fourth[0]]


def doubleEliminationTournamentWBC(sigmaProb: float, players: list[float | int]) -> list[int]:
    indexed_players = list(enumerate(players))

    def match(a, b):
        r = isWin(sigmaProb, a[1], b[1])
        return (a, b) if r == 1 else (b, a)  # (勝者, 敗者)

    winners_bracket = indexed_players.copy()
    losers_bracket = []

    # 勝者側・敗者側を交互に進める
    while len(winners_bracket) > 2:
        # 勝者側1ラウンド
        next_winners = []
        new_losers = []
        for i in range(len(winners_bracket) // 2):
            winner, loser = match(winners_bracket[i], winners_bracket[i + len(winners_bracket) // 2])
            next_winners.append(winner)
            new_losers.append(loser)
        winners_bracket = next_winners

        # 敗者側：既存の敗者同士で1ラウンド戦ってから新規敗者と合流
        if losers_bracket:
            next_losers = []
            for i in range(len(losers_bracket) // 2):
                winner, _ = match(losers_bracket[i], losers_bracket[i + len(losers_bracket) // 2])
                next_losers.append(winner)
            losers_bracket = next_losers

        losers_bracket.extend(new_losers)

    # 敗者側決勝（4位はここの敗者）
    losers_finalist, fourth = match(losers_bracket[0], losers_bracket[1])

    # 勝者側決勝
    winners_finalist, winners_loser = match(winners_bracket[0], winners_bracket[1])
    losers_bracket.append(winners_loser)

    # 負けたら3位、勝ったら大決勝
    second_candidate, third = match(winners_loser, losers_finalist)

    # 大決勝(1回しか行わない)
    first, second = match(winners_finalist, second_candidate)

    return [first[0], second[0], third[0], fourth[0]]


def countCorrectRankings(rank: list[int], results: list[int]) -> list[int]:
    """上位4人が正しく順位付けされた回数を集計する"""
    r1, r2, r3, r4 = results
    return [
        rank[r1] == 1,
        rank[r1] == 2 or rank[r2] == 2,
        rank[r1] == 3 or rank[r2] == 3 or rank[r3] == 3,
        rank[r1] == 4 or rank[r2] == 4 or rank[r3] == 4 or rank[r4] == 4,
    ]


def runTrial(args):
    playerCount, sigmaProb, tryCount = args
    # counts = {name: [0] * 4 for name in ["tournament", "swiss", "roundRobin"]}
    counts = {name: [0] * 4 for name in ["tournament", "doubleEliminationTournament", "doubleEliminationTournamentWBC"]}

    for _ in range(tryCount):
        players = [random.gauss(0.0, 1.0) for _ in range(playerCount)]
        rank = getRank(players)

        # for name, func in [("tournament", tournament), ("swiss", swissTournament), ("roundRobin", roundRobinTournament)]:
        for name, func in [("tournament", tournament), ("doubleEliminationTournament", doubleEliminationTournament), ("doubleEliminationTournamentWBC", doubleEliminationTournamentWBC)]:
            correct = countCorrectRankings(rank, func(sigmaProb, players))
            for i in range(4):
                counts[name][i] += correct[i]

    return counts


def runSimulation(tryCount: int = 1000000, workers: int = 8):
    chunkSize = tryCount // workers

    for playerCount in [4, 8, 16, 32]:
        for sigmaProb in [0.51, 0.55, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99, 0.999, 0.9999]:
            args = [(playerCount, sigmaProb, chunkSize)] * workers

            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = executor.map(runTrial, args)

            # 集計
            # counts = {name: [0] * 4 for name in ["tournament", "swiss", "roundRobin"]}
            counts = {name: [0] * 4 for name in ["tournament", "doubleEliminationTournament", "doubleEliminationTournamentWBC"]}
            for result in results:
                for name in counts:
                    for i in range(4):
                        counts[name][i] += result[name][i]

            total = chunkSize * workers
            for name in counts:
                rates = [counts[name][i] / total for i in range(4)]
                print(playerCount, sigmaProb, name, *rates)
            print()


if __name__ == "__main__":
    runSimulation()
