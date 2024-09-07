from fractions import Fraction
from dataclasses import dataclass
from functools import reduce
from math import ceil, floor
from typing import Optional
import itertools
import json
import gameResult
import sys


TEAM_COUNT = 6

@dataclass(frozen=True)
class Game:
    win: int
    lose: int
    draw: int
    remain: int

    def __init__(self, win: int, lose: int, draw: int, remain: int) -> None:
        if win < 0 or lose < 0 or draw < 0 or remain < 0:
            raise ValueError("Exists negative number.")

        object.__setattr__(self, "win", win)
        object.__setattr__(self, "lose", lose)
        object.__setattr__(self, "draw", draw)
        object.__setattr__(self, "remain", remain)

    def __add__(self, other):
        return Game(
            self.win + other.win,
            self.lose + other.lose,
            self.draw + other.draw,
            self.remain + other.remain,
        )

    def getProbability(self) -> Fraction:
        return Fraction(self.win, self.win + self.lose)

    def getAllRemainWin(self): # Self
        return Game(self.win + self.remain, self.lose, self.draw, 0)

    def getAllRemainLose(self): # Self
        return Game(self.win, self.lose + self.remain, self.draw, 0)

    def getDualGame(self): # Self
        return Game(self.lose, self.win, self.draw, self.remain)


@dataclass(frozen=True)
class Team:
    opponents: tuple[Game, ...]

    def __init__(self, opponents: tuple[Game, ...]) -> None:
        object.__setattr__(self, "opponents", opponents)

    def getNowWin(self) -> Fraction:
        return reduce(lambda x, y: x + y, self.opponents, Game(0, 0, 0, 0)).getProbability()

    def getMaxWin(self) -> Fraction:
        return reduce(lambda x, y: x + y, self.opponents, Game(0, 0, 0, 0)).getAllRemainWin().getProbability()

    def getMinWin(self) -> Fraction:
        return reduce(lambda x, y: x + y, self.opponents, Game(0, 0, 0, 0)).getAllRemainLose().getProbability()

    def getWinningCountToProbability(self, probability: Fraction) -> Optional[int]:
        # 全部勝っても到達できない場合
        reduced = reduce(lambda x, y: x + y, self.opponents, Game(0, 0, 0, 0))
        if Fraction(reduced.win + reduced.remain, reduced.win + reduced.lose + reduced.remain) < probability:
            return None

        count = probability * Fraction(reduced.win + reduced.lose + reduced.remain) - Fraction(reduced.win)

        # 確定している場合
        if count < 0:
            return None

        return ceil(count)

    def getLoseIndexOpponent(self, index: int): # Self
        game = self.opponents[index]
        return Team(tuple((self.opponents[:index] + (Game(game.win, game.lose + game.remain, game.draw, 0), ) + self.opponents[index + 1:])))

    def getDeletedIndexOpponent(self, index: int): # Self
        return Team(tuple(self.opponents[:index] + self.opponents[index + 1:-1] + (self.opponents[index] + self.opponents[-1], )))

    def getReplacedIndexGameWithWinLose(self, index: int, win: int, lose: int): # Self
        game = self.opponents[index]
        return Team(tuple(self.opponents[:index] + (Game(game.win + win, game.lose + lose, game.draw + game.remain - win - lose, 0), ) + self.opponents[index + 1:]))

    def getDualTeam(self): # Self
        return Team(tuple(map(lambda game: game.getDualGame(), self.opponents)))


@dataclass(frozen=True)
class Table:
    teams: tuple[Team, ...]

    def __init__(self, teams: tuple[Team, ...]) -> None:
        object.__setattr__(self, "teams", teams)

    def getSelfVictory(self, index: int) -> Fraction:
        win = Fraction(0, 1)
        for i, team in enumerate(self.teams):
            if i == index:
                continue

            p = team.getLoseIndexOpponent(index).getMaxWin()
            if p > win:
                win = p

        return win

    def getMaxWin1(self, index: int) -> Fraction:
        win = Fraction(0, 1)
        for team in self.__transform(index).teams:
            if team.getMaxWin() > win:
                win = team.getMaxWin()

        return win

    def getMaxWin2(self, index: int) -> Fraction:
        win = Fraction(0, 1)
        transformedTable = self.__transform(index)
        count = len(transformedTable.teams)

        for t1, t2 in itertools.combinations(range(count), 2):
            game = transformedTable.teams[t1].opponents[t2]
            for w12, w21 in self.__iterWin2(game.remain):
                minProbability = min(
                    transformedTable.teams[t1].getReplacedIndexGameWithWinLose(t2, w12, w21).getMaxWin(),
                    transformedTable.teams[t2].getReplacedIndexGameWithWinLose(t1, w21, w12).getMaxWin(),
                )

            if minProbability > win:
                win = minProbability

        return win

    def getMaxWin3(self, index: int) -> Fraction:
        win = Fraction(0, 1)
        transformedTable = self.__transform(index)
        count = len(transformedTable.teams)

        for t1, t2, t3 in itertools.combinations(range(count), 3):
            iterWin3 = self.__iterWin3(
                transformedTable.teams[t1].opponents[t2].remain,
                transformedTable.teams[t1].opponents[t3].remain,
                transformedTable.teams[t2].opponents[t3].remain,
            )

            for w12, w13, w21, w23, w31, w32 in iterWin3:
                minProbability = min(
                    transformedTable.teams[t1].getReplacedIndexGameWithWinLose(t2, w12, w21).getMaxWin(),
                    transformedTable.teams[t1].getReplacedIndexGameWithWinLose(t3, w13, w31).getMaxWin(),
                    transformedTable.teams[t2].getReplacedIndexGameWithWinLose(t1, w21, w12).getMaxWin(),
                    transformedTable.teams[t2].getReplacedIndexGameWithWinLose(t3, w23, w32).getMaxWin(),
                    transformedTable.teams[t3].getReplacedIndexGameWithWinLose(t1, w31, w13).getMaxWin(),
                    transformedTable.teams[t3].getReplacedIndexGameWithWinLose(t2, w32, w23).getMaxWin(),
                )

            if minProbability > win:
                win = minProbability

        return win

    def getDualTable(self): # Self
        return Table(tuple(map(lambda team: team.getDualTeam(), self.teams)))

    def __transform(self, index: int): # Self
        return Table(tuple(map(lambda team: team.getDeletedIndexOpponent(index), self.teams[:index] + self.teams[index + 1:])))

    def __iterWin2(self, remain: int) -> list[tuple[int, int]]:
        result = []
        for i in range(remain + 1):
            for j in range(remain - i + 1):
                result.append((i, j))

        return result

    def __iterWin3(self, remain12: int, remain13: int, remain23: int) -> list[tuple[int, int, int, int, int, int]]:
        result = []
        for wl12, wl13, wl23 in itertools.product(self.__iterWin2(remain12), self.__iterWin2(remain13), self.__iterWin2(remain23)):
            result.append((wl12[0], wl13[0], wl12[1], wl23[0], wl13[1], wl23[1]))

        return result

def getResult(originalTable, setting):
    table = Table(tuple(Team(tuple(Game(opponent["w"], opponent["l"], opponent["d"], opponent["r"]) for opponent in team)) for team in originalTable))
    dualTable = table.getDualTable()

    result = [{
        "index": i,
        "max": table.teams[i].getMaxWin(),
        "now": table.teams[i].getNowWin(),
        "min": table.teams[i].getMinWin(),
        "win1": table.getMaxWin1(i),
        "win2": table.getMaxWin2(i),
        "win3": table.getMaxWin3(i),
        "selfV": table.getSelfVictory(i),
        "lose1": dualTable.getMaxWin1(i),
        "lose2": dualTable.getMaxWin2(i),
        "lose3": dualTable.getMaxWin3(i),
    } for i in range(TEAM_COUNT)]

    response = [{
        "index": team["index"],
        "name": setting[team["index"]]["name"],
        "color": setting[team["index"]]["color"],
        "max": floor(team["max"] * Fraction(1000)),
        "now": floor(team["now"] * Fraction(1000)),
        "min": floor(team["min"] * Fraction(1000)),
        "win1": floor(team["win1"] * Fraction(1000)),
        "win2": floor(team["win2"] * Fraction(1000)),
        "win3": floor(team["win3"] * Fraction(1000)),
        "selfV": floor(team["selfV"] * Fraction(1000)),
        "canSelfV": team["selfV"] < team["max"],
        "lose1": floor((Fraction(1) - team["lose1"]) * Fraction(1000)),
        "lose2": floor((Fraction(1) - team["lose2"]) * Fraction(1000)),
        "lose3": floor((Fraction(1) - team["lose3"]) * Fraction(1000)),
        "win1Magic": table.teams[team["index"]].getWinningCountToProbability(team["win1"]),
        "win2Magic": table.teams[team["index"]].getWinningCountToProbability(team["win2"]),
        "win3Magic": table.teams[team["index"]].getWinningCountToProbability(team["win3"]),
        "lose1Magic": (lambda x: -1 * x if x is not None else None)(dualTable.teams[team["index"]].getWinningCountToProbability(team["lose1"])),
        "lose2Magic": (lambda x: -1 * x if x is not None else None)(dualTable.teams[team["index"]].getWinningCountToProbability(team["lose2"])),
        "lose3Magic": (lambda x: -1 * x if x is not None else None)(dualTable.teams[team["index"]].getWinningCountToProbability(team["lose3"])),
    } for team in result]

    return sorted(response, key = lambda x: x['now'], reverse = True)

date = sys.argv[1]
with open("data.txt", mode='a') as f:
    centralData = gameResult.getCentralData(date)
    pacificData = gameResult.getPacificData(date)
    centralResult = getResult(centralData["result"], centralData["setting"])
    pacificResult = getResult(pacificData["result"], pacificData["setting"])

    centralDisplayData = {
        'league': 'central',
        'date': date,
        'displayData': centralResult,
    }

    pacificDisplayData = {
        'league': 'pacific',
        'date': date,
        'displayData': pacificResult,
    }

    f.write(json.dumps(centralDisplayData) + '\n')
    f.write(json.dumps(pacificDisplayData) + '\n')
