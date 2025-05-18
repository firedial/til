import math
from dataclasses import dataclass
from fractions import Fraction
import concurrent.futures


@dataclass(frozen=True)
class WinningRate:
    win: int
    lose: int

    def __init__(self, win: int, lose: int) -> None:
        if win < 0 or lose < 0:
            raise ValueError("Exists negative number.")

        if win + lose == 0:
            raise ValueError("No game.")

        object.__setattr__(self, "win", win)
        object.__setattr__(self, "lose", lose)

    def rate(self) -> Fraction:
        return Fraction(self.win, self.win + self.lose)

    def dualRate(self) -> Fraction:
        return Fraction(self.lose, self.win + self.lose)

    def __lt__(self, other):
        return self.win * other.lose - self.lose * other.win < 0

@dataclass(frozen=True)
class Game:
    win: int
    lose: int

    def __init__(self, win: int, lose: int) -> None:
        if win < 0 or lose < 0:
            raise ValueError("Exists negative number.")

        object.__setattr__(self, "win", win)
        object.__setattr__(self, "lose", lose)

    def getDualGame(self):
        return Game(self.lose, self.win)


@dataclass(frozen=True)
class Remain:
    remain: tuple[int, ...]

    def __init__(self, remain: tuple[int, ...]) -> None:
        if len(remain) != 7:
            raise ValueError("Length is not 7.")

        if remain[0] < 0 or remain[1] < 0 or remain[2] < 0 or remain[3] < 0 or remain[4] < 0 or remain[5] < 0 or remain[6] < 0:
            raise ValueError("Exists negative number.")

        object.__setattr__(self, "remain", remain)

    def removedRemain(self, removeIndexes: list[int]) -> int:
        remainCount = 0
        for i, r in enumerate(self.remain):
            if i not in removeIndexes:
                remainCount += r

        return remainCount


@dataclass(frozen=True)
class Table:
    games: list[Game]
    remains: list[Remain]

    def __init__(self, games: list[Game], remains: list[Remain]) -> None:
        if len(games) != 6 or len(remains) != 6:
            raise ValueError("Length is not 6.")

        object.__setattr__(self, "games", games)
        object.__setattr__(self, "remains", remains)

    def getDualTable(self):
        return Table(
            list(map(lambda game: game.getDualGame(), self.games)),
            self.remains,
        )

    def getSelfV(self, t1: int) -> WinningRate:
        maxSelfV = WinningRate(0, 1)

        for i in range(6):
            if i == t1:
                continue

            maxSelfV = max(maxSelfV, WinningRate(self.games[i].win + self.remains[i].removedRemain([t1]), self.games[i].lose + self.remains[i].remain[t1]))

        return maxSelfV

    def getNow(self, t1: int) -> WinningRate:
        return WinningRate(self.games[t1].win, self.games[t1].lose)

    def getWin1(self, t1: int) -> WinningRate:
        return WinningRate(self.games[t1].win + self.remains[t1].removedRemain([]), self.games[t1].lose)

    def getWin2(self, t1: int, t2: int) -> WinningRate:
        r1 = self.remains[t1].removedRemain([t2])
        r2 = self.remains[t2].removedRemain([t1])

        # init に入れてもいいかも
        assert self.remains[t1].remain[t2] == self.remains[t2].remain[t1]

        return self.__getMaxMin2(self.games[t1].win + r1, self.games[t1].lose, self.games[t2].win + r2, self.games[t2].lose, self.remains[t1].remain[t2])

    def getWin3(self, t1: int, t2: int, t3: int) -> WinningRate:
        r1 = self.remains[t1].removedRemain([t2, t3])
        r2 = self.remains[t2].removedRemain([t1, t3])
        r3 = self.remains[t3].removedRemain([t1, t2])

        r12 = self.remains[t1].remain[t2]
        r13 = self.remains[t1].remain[t3]
        r23 = self.remains[t2].remain[t3]

        maxMin3 = WinningRate(0, 1)
        for w12 in range(r12 + 1):
            for l12 in range(r12 + 1 - w12):
                for w13 in range(r13 + 1):
                    for l13 in range(r13 + 1 - w13):
                        winningRate1 = WinningRate(self.games[t1].win + w12 + w13 + r1, self.games[t1].lose + l12 + l13)
                        maxMin2 = self.__getMaxMin2(self.games[t2].win + l12 + r2, self.games[t2].lose + w12, self.games[t3].win + l13 + r3, self.games[t3].lose + w13, r23)
                        maxMin3 = max(maxMin3, min(maxMin2, winningRate1))

        return maxMin3

    def __getMaxMin2(self, w1: int, l1: int, w2: int, l2: int, r: int) -> WinningRate:
        min2judge2 = lambda w, l: min(WinningRate(w1 + w, l1 + l), WinningRate(w2 + l, l2 + w))
        min2judge4 = lambda w, l: min(WinningRate(w1 + w, l1 + l), WinningRate(w2 + l, l2 + w), WinningRate(w1 + w, l1 + l + 1), WinningRate(w2 + l + 1, l2 + w))

        maxMin2 = WinningRate(0, 1)
        for w in range(r + 1):
            d2 = (l1 - w2) ** 2 - 4 * (w1 + w) * (l2 + w)

            if d2 < 0:
                maxMin2 = max(maxMin2, min2judge2(w, 0), min2judge2(2, r - w))
                continue

            l = (-1 * (l1 - w2) + math.sqrt(d2)) / 2
            floorL = math.floor(l)

            if l < 0 or w + l >= r:
                maxMin2 = max(maxMin2, min2judge2(w, 0), min2judge2(2, r - w))
                continue

            maxMin2 = max(maxMin2, min2judge4(w, floorL))

        return maxMin2

    def getWinMagic(self, t1: int, rate: WinningRate) -> int|None:
        w1 = self.games[t1].win
        l1 = self.games[t1].lose
        r1 = self.remains[t1].removedRemain([])

        wt = rate.win
        lt = rate.lose

        a = (l1 + r1) * wt - w1 * lt
        b = lt + wt

        w = a // b if a % b == 0 else (a // b) + 1
        return None if w < 0 else w


def getMaxWinT1(count: int, maxWin: dict, t1: int) -> WinningRate:
    maxWinByT1 = WinningRate(0, 1)
    for key, value in maxWin.items():
        if len(key) != count:
            continue

        if t1 not in key:
            continue

        maxWinByT1 = max(maxWinByT1, value)

    return maxWinByT1


def calc():
    games = [
        Game(1, 1),
        Game(1, 1),
        Game(1, 1),
        Game(1, 1),
        Game(1, 1),
        Game(1, 1),
    ]

    remains = [
        Remain((0, 5, 5, 2, 1, 5, 1)),
        Remain((5, 0, 5, 2, 1, 5, 1)),
        Remain((5, 5, 0, 2, 1, 5, 1)),
        Remain((2, 2, 2, 0, 1, 5, 1)),
        Remain((1, 1, 1, 1, 0, 5, 1)),
        Remain((5, 5, 5, 5, 5, 0, 1)),
    ]

    remains = [
        Remain((0, 25, 25, 25, 25, 25, 16)),
        Remain((25, 0, 25, 25, 25, 25, 16)),
        Remain((25, 25, 0, 25, 25, 25, 16)),
        Remain((25, 25, 25, 0, 25, 25, 16)),
        Remain((25, 25, 25, 25, 0, 25, 16)),
        Remain((25, 25, 25, 25, 25, 0, 16)),
    ]

    t1ss = [
        [0],
        [1],
        [2],
        [3],
        [4],
        [5],
    ]

    t2ss = [
        [0, 1],
        [0, 2],
        [0, 3],
        [0, 4],
        [0, 5],
        [1, 2],
        [1, 3],
        [1, 4],
        [1, 5],
        [2, 3],
        [2, 4],
        [2, 5],
        [3, 4],
        [3, 5],
        [4, 5],
    ]

    t3ss = [
        [0, 1, 2],
        [0, 1, 3],
        [0, 1, 4],
        [0, 1, 5],
        [0, 2, 3],
        [0, 2, 4],
        [0, 2, 5],
        [0, 3, 4],
        [0, 3, 5],
        [0, 4, 5],
        [1, 2, 3],
        [1, 2, 4],
        [1, 2, 5],
        [1, 3, 4],
        [1, 3, 5],
        [1, 4, 5],
        [2, 3, 4],
        [2, 3, 5],
        [2, 4, 5],
        [3, 4, 5],
    ]

    table = Table(games, remains)

    selfV: list[WinningRate] = []
    for t1s in t1ss:
        selfV.append(table.getSelfV(t1s[0]))

    winMax: dict[frozenset, WinningRate] = {}
    for t1s in t1ss:
        winMax[frozenset(t1s)] = table.getWin1(t1s[0])
    for t2s in t2ss:
        winMax[frozenset(t2s)] = table.getWin2(t2s[0], t2s[1])
    # for t3s in t3ss:
    #     winMax[frozenset(t3s)] = table.getWin3(t3s[0], t3s[1], t3s[2])

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for t3s, result in zip(t3ss, executor.map(table.getWin3, list(map(lambda x: x[0], t3ss)), list(map(lambda x: x[1], t3ss)), list(map(lambda x: x[2], t3ss)))):
            winMax[frozenset(t3s)] = result

    dualTable = table.getDualTable()
    loseMin: dict[frozenset, WinningRate] = {}
    for t1s in t1ss:
        loseMin[frozenset(t1s)] = table.getWin1(t1s[0])
    for t2s in t2ss:
        loseMin[frozenset(t2s)] = table.getWin2(t2s[0], t2s[1])
    # for t3s in t3ss:
    #     loseMin[frozenset(t3s)] = table.getWin3(t3s[0], t3s[1], t3s[2])

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for t3s, result in zip(t3ss, executor.map(dualTable.getWin3, list(map(lambda x: x[0], t3ss)), list(map(lambda x: x[1], t3ss)), list(map(lambda x: x[2], t3ss)))):
            loseMin[frozenset(t3s)] = result

    data = []
    for t1 in range(6):
        win1 = getMaxWinT1(1, winMax, t1)
        win2 = getMaxWinT1(2, winMax, t1)
        win3 = getMaxWinT1(3, winMax, t1)

        lose1 = getMaxWinT1(1, loseMin, t1)
        lose2 = getMaxWinT1(2, loseMin, t1)
        lose3 = getMaxWinT1(3, loseMin, t1)

        data.append(
            {
                "league": "t",
                "index": t1,
                "max": winMax[frozenset([t1])].rate(),
                "now": table.getNow(t1).rate(),
                "min": loseMin[frozenset([t1])].dualRate(),
                "selfV": selfV[t1].rate(),
                "canSelfV": selfV[t1].rate() <= winMax[frozenset([t1])].rate(),
                "win1": win1.rate(),
                "win2": win2.rate(),
                "win3": win3.rate(),
                "lose1": lose1.dualRate(),
                "lose2": lose2.dualRate(),
                "lose3": lose3.dualRate(),
                "win1Magic": table.getWinMagic(t1, win1),
                "win2Magic": table.getWinMagic(t1, win2),
                "win3Magic": table.getWinMagic(t1, win3),
                "lose1Magic": table.getWinMagic(t1, lose1),
                "lose2Magic": table.getWinMagic(t1, lose2),
                "lose3Magic": table.getWinMagic(t1, lose3),
            }
        )

    return data


def main():
    data = calc()

    return list(map(lambda d: [
        d["league"],
        d["index"],
        str(round(d["max"] * 1000)).zfill(3),
        str(round(d["now"] * 1000)).zfill(3),
        str(round(d["min"] * 1000)).zfill(3),
        str(round(d["selfV"] * 1000)).zfill(3),
        "t" if d["canSelfV"] else "f",
        str(round(d["win1"] * 1000)).zfill(3),
        str(round(d["win2"] * 1000)).zfill(3),
        str(round(d["win3"] * 1000)).zfill(3),
        str(d["win1Magic"]) if d["win1Magic"] is not None else "n",
        str(d["win2Magic"]) if d["win2Magic"] is not None else "n",
        str(d["win3Magic"]) if d["win3Magic"] is not None else "n",
        str(round(d["lose1"] * 1000)).zfill(3),
        str(round(d["lose2"] * 1000)).zfill(3),
        str(round(d["lose3"] * 1000)).zfill(3),
        str(-1 * d["lose1Magic"]) if d["lose1Magic"] is not None else "n",
        str(-1 * d["lose2Magic"]) if d["lose2Magic"] is not None else "n",
        str(-1 * d["lose3Magic"]) if d["lose3Magic"] is not None else "n",
    ], data))


print(main())


