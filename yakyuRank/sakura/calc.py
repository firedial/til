import math
from dataclasses import dataclass
from fractions import Fraction
import concurrent.futures
import csv
import datetime
import sys


@dataclass(frozen=True)
class WinningRate:
    win: int
    lose: int

    def __init__(self, win: int, lose: int) -> None:
        if win < 0 or lose < 0:
            raise ValueError("Exists negative number.")

        object.__setattr__(self, "win", win)
        object.__setattr__(self, "lose", lose)

    def rate(self) -> Fraction:
        if self.win + self.lose == 0:
            return Fraction(0, 1)
        return Fraction(self.win, self.win + self.lose)

    def dualRate(self) -> Fraction:
        if self.win + self.lose == 0:
            return Fraction(1, 1)
        return Fraction(self.lose, self.win + self.lose)

    def __lt__(self, other):
        return self.win * other.lose - self.lose * other.win < 0

@dataclass(frozen=True)
class Game:
    win: int
    lose: int
    draw: int

    def __init__(self, win: int, lose: int, draw: int) -> None:
        if win < 0 or lose < 0:
            raise ValueError("Exists negative number.")

        object.__setattr__(self, "win", win)
        object.__setattr__(self, "lose", lose)
        object.__setattr__(self, "draw", draw)

    def getDualGame(self):
        return Game(self.lose, self.win, self.draw)


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

        if t1 in key:
            continue

        maxWinByT1 = max(maxWinByT1, value)

    return maxWinByT1


def calcWinMax(table: Table):
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

    return winMax


def calc(table: Table, winMax, loseMin):
    dualTable = table.getDualTable()

    selfV: list[WinningRate] = []
    for t1s in [[0], [1], [2], [3], [4], [5]]:
        selfV.append(table.getSelfV(t1s[0]))

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
                "lose1Magic": dualTable.getWinMagic(t1, lose1),
                "lose2Magic": dualTable.getWinMagic(t1, lose2),
                "lose3Magic": dualTable.getWinMagic(t1, lose3),
                "winCount": table.games[t1].win,
                "loseCount": table.games[t1].lose,
                "drawCount": table.games[t1].draw,
            }
        )

    sortedData = sorted(data, key = lambda x: x["now"], reverse = True)
    resultData = []
    for i, data in enumerate(sortedData):
        data["rank"] = i + 1
        resultData.append(data)

    return resultData

def getGameResult(targetDate: str, league: str):
    teamData = {
        "c": {"G": 0, "T": 1, "DB": 2, "C": 3, "S": 4, "D": 5, "O": 6},
        "p": {"H": 0, "F": 1, "M": 2, "E": 3, "B": 4, "L": 5, "O": 6},
    }

    games = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]

    remains = [
        [0, 25, 25, 25, 25, 25, 18],
        [25, 0, 25, 25, 25, 25, 18],
        [25, 25, 0, 25, 25, 25, 18],
        [25, 25, 25, 0, 25, 25, 18],
        [25, 25, 25, 25, 0, 25, 18],
        [25, 25, 25, 25, 25, 0, 18],
        [0, 0, 0, 0, 0, 0, 108],
    ]

    targetDate = datetime.datetime.strptime(targetDate, "%Y-%m-%d")
    with open("result.csv") as f:
        for column in csv.reader(f):
            resultDate = datetime.datetime.strptime(column[0], "%Y-%m-%d")
            if targetDate < resultDate:
                continue

            if column[1] != league:
                continue

            t1 = teamData[league][column[2]]
            t2 = teamData[league][column[3]]

            remains[t1][t2] -= 1
            remains[t2][t1] -= 1

            gameResult = column[4]
            if gameResult == "d":
                games[t1][2] += 1 # 引き分け
                games[t2][2] += 1 # 引き分け
            elif gameResult == "w":
                games[t1][0] += 1 # 勝ち
                games[t2][1] += 1 # 負け
            elif gameResult == "l":
                games[t1][1] += 1 # 負け
                games[t2][0] += 1 # 勝ち
            else:
                raise Exception("game result is wrong")

    # 最後の要素を削除する
    games.pop()
    remains.pop()

    return list(map(lambda x: Game(x[0], x[1], x[2]), games)), list(map(lambda x: Remain(tuple(x)), remains))


def leagueMain(league: str, targetDate: str):
    games, remains = getGameResult(targetDate, league)

    table = Table(games, remains)
    dualTable = table.getDualTable()

    # とり得る値の最大値と最小値
    with open("winMax.csv", mode='r') as f:
        for column in csv.reader(f):
            if column[0] == targetDate and column[1] == league:
                winMax = eval(column[2])
                break
        else:
            winMax = calcWinMax(table)
            with open("winMax.csv", mode='a') as g:
                g.write(targetDate + ',' + league + ',' + '"' + str(winMax) + '"' + '\n')
    with open("loseMin.csv", mode='r') as f:
        for column in csv.reader(f):
            if column[0] == targetDate and column[1] == league:
                loseMin = eval(column[2])
                break
        else:
            loseMin = calcWinMax(dualTable)
            with open("loseMin.csv", mode='a') as g:
                g.write(targetDate + ',' + league + ',' + '"' + str(loseMin) + '"' + '\n')

    result = calc(table, winMax, loseMin)

    data = list(map(lambda d: [
        targetDate,
        league,
        str(d["index"]),
        str(round(d["max"] * 1000)),
        str(round(d["now"] * 1000)),
        str(round(d["min"] * 1000)),
        str(round(d["selfV"] * 1000)),
        "t" if d["canSelfV"] else "f",
        str(round(d["win1"] * 1000)),
        str(round(d["win2"] * 1000)),
        str(round(d["win3"] * 1000)),
        str(d["win1Magic"]) if d["win1Magic"] is not None else "n",
        str(d["win2Magic"]) if d["win2Magic"] is not None else "n",
        str(d["win3Magic"]) if d["win3Magic"] is not None else "n",
        str(round(d["lose1"] * 1000)),
        str(round(d["lose2"] * 1000)),
        str(round(d["lose3"] * 1000)),
        str(d["lose1Magic"]) if d["lose1Magic"] is not None else "n",
        str(d["lose2Magic"]) if d["lose2Magic"] is not None else "n",
        str(d["lose3Magic"]) if d["lose3Magic"] is not None else "n",
        str(d["rank"]),
        str(d["winCount"]),
        str(d["loseCount"]),
        str(d["drawCount"]),
        str(143 - d["winCount"] - d["loseCount"] - d["drawCount"]),
    ], result))


    return "\n".join(list(map(lambda x: ",".join(x), data))) + "\n"


def main():
    # 試合結果に入っている日付
    centralDateList = set()
    pacificDateList = set()
    centralDateList.add("2025-01-01")
    pacificDateList.add("2025-01-01")
    with open("result.csv") as f:
        for column in csv.reader(f):
            if column[1] == "c":
                centralDateList.add(column[0])
            elif column[1] == "p":
                pacificDateList.add(column[0])

    # 未集計の日付で集計していく
    dataString = ""
    for targetDate in sorted(list(centralDateList | pacificDateList)):
        if targetDate in centralDateList:
            data = leagueMain("c", targetDate)
            if data is None:
                continue
            dataString += data
        if targetDate in pacificDateList:
            data = leagueMain("p", targetDate)
            if data is None:
                continue
            dataString += data

    with open("data.csv", mode='w') as f:
        f.write(dataString)


def updateResult(data: str):
    C = ["G", "T", "Z", "C", "S", "D", "O"]
    P = ["H", "F", "M", "E", "B", "L", "O"]

    l = data.split(",")
    resultData = ""

    for rawDate, result in zip(l[0::2], l[1::2]):
        date = datetime.datetime.strptime(rawDate, "%Y-%m-%d").strftime("%Y-%m-%d")

        for t1, t2, r in zip(result[0::3], result[1::3], result[2::3]):
            if t1 in C:
                league = "c"
                group = C
            elif t1 in P:
                league = "p"
                group = P
            else:
                raise ValueError("no league.")

            if t1 not in group:
                raise ValueError("wrong team.")
            if t2 not in group:
                raise ValueError("wrong team.")
            if r not in ["w", "l", "d"]:
                raise ValueError("wrong result.")

            if t1 == "Z":
                t1 = "DB"
            if t2 == "Z":
                t2 = "DB"

            resultData += ','.join([date, league, t1, t2, r]) + "\n"

    with open("result.csv", mode='a') as f:
        f.write(resultData)

if len(sys.argv) == 2:
    updateResult(sys.argv[1])

main()
