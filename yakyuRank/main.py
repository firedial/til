from fractions import Fraction
from dataclasses import dataclass
from functools import reduce
from math import ceil, floor
from typing import Optional
import json


# 2024/8/26 終了時点

originalTable = [
    [ # 広島
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 8, "l": 8, "d": 3, "r": 6},
        {"w": 11, "l": 10, "d": 1, "r": 3},
        {"w": 13, "l": 6, "d": 0, "r": 6},
        {"w": 7, "l": 11, "d": 1, "r": 6},
        {"w": 11, "l": 5, "d": 0, "r": 9},
        {"w": 10, "l": 8, "d": 0, "r": 0},
    ],
    [ # 巨人
        {"w": 8, "l": 8, "d": 3, "r": 6},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 10, "l": 10, "d": 1, "r": 4},
        {"w": 12, "l": 6, "d": 0, "r": 7},
        {"w": 12, "l": 9, "d": 1, "r": 3},
        {"w": 12, "l": 7, "d": 0, "r": 6},
        {"w": 8, "l": 9, "d": 1, "r": 0},
    ],
    [ # 阪神
        {"w": 10, "l": 11, "d": 1, "r": 3},
        {"w": 10, "l": 10, "d": 1, "r": 4},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 9, "l": 8, "d": 1, "r": 7},
        {"w": 11, "l": 7, "d": 3, "r": 4},
        {"w": 11, "l": 8, "d": 0, "r": 6},
        {"w": 7, "l": 11, "d": 0, "r": 0},
    ],
    [ # DeNA
        {"w": 6, "l": 13, "d": 0, "r": 6},
        {"w": 6, "l": 12, "d": 0, "r": 7},
        {"w": 8, "l": 9, "d": 1, "r": 7},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 12, "l": 7, "d": 1, "r": 5},
        {"w": 14, "l": 9, "d": 0, "r": 2},
        {"w": 11, "l": 7, "d": 0, "r": 0},
    ],
    [ # 中日
        {"w": 11, "l": 7, "d": 1, "r": 6},
        {"w": 9, "l": 12, "d": 1, "r": 3},
        {"w": 7, "l": 11, "d": 3, "r": 4},
        {"w": 7, "l": 12, "d": 1, "r": 5},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 9, "l": 9, "d": 2, "r": 5},
        {"w": 7, "l": 11, "d": 0, "r": 0},
    ],
    [ # ヤクルト
        {"w": 5, "l": 11, "d": 0, "r": 9},
        {"w": 7, "l": 12, "d": 0, "r": 6},
        {"w": 8, "l": 11, "d": 0, "r": 6},
        {"w": 9, "l": 14, "d": 0, "r": 2},
        {"w": 9, "l": 9, "d": 2, "r": 5},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 9, "l": 7, "d": 2, "r": 0},
    ],
]


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

    def getReplacedIndexGame(self, index: int, game: Game): # Self
        return Team(tuple(self.opponents[:index] + (game, ) + self.opponents[index + 1:]))

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

        for i in range(count):
            for j in range(i + 1, count):
                game = transformedTable.teams[i].opponents[j]
                r = game.remain
                for w in range(r + 1):
                    for l in range(r - w + 1):
                        minProbability = min(
                            transformedTable.teams[i].getReplacedIndexGame(j, Game(game.win + w, game.lose + l, game.draw + r - w - l, 0)).getMaxWin(),
                            transformedTable.teams[j].getReplacedIndexGame(i, Game(game.lose + l, game.win + w, game.draw + r - w - l, 0)).getMaxWin(),
                        )

                if minProbability > win:
                    win = minProbability

        return win

    def getMaxWin3(self, index: int) -> Fraction:
        win = Fraction(0, 1)
        transformedTable = self.__transform(index)
        count = len(transformedTable.teams)

        for i in range(count):
            for j in range(i + 1, count):
                for k in range(j + 1, count):
                    gameIJ = transformedTable.teams[i].opponents[j]
                    gameJK = transformedTable.teams[j].opponents[k]
                    gameKI = transformedTable.teams[k].opponents[i]

                    rIJ = gameIJ.remain
                    rJK = gameJK.remain
                    rKI = gameKI.remain
                    for wI in range(rIJ + 1):
                        for lI in range(rIJ - wI + 1):
                            for wJ in range(rJK + 1):
                                for lJ in range(rJK - wJ + 1):
                                    for wK in range(rKI + 1):
                                        for lK in range(rKI - wK + 1):

                                            minProbability = min(
                                                transformedTable.teams[i].getReplacedIndexGame(j, Game(gameIJ.win + wI, gameIJ.lose + lI, gameIJ.draw + rIJ - wI - lI, 0)).getReplacedIndexGame(k, Game(gameKI.lose + lK, gameKI.win + wK, gameKI.draw + rKI - wK - lK, 0)).getMaxWin(),
                                                transformedTable.teams[j].getReplacedIndexGame(k, Game(gameJK.win + wJ, gameJK.lose + lJ, gameJK.draw + rJK - wJ - lJ, 0)).getReplacedIndexGame(i, Game(gameIJ.lose + lI, gameIJ.win + wI, gameIJ.draw + rIJ - wI - lI, 0)).getMaxWin(),
                                                transformedTable.teams[k].getReplacedIndexGame(i, Game(gameKI.win + wK, gameKI.lose + lK, gameKI.draw + rKI - wK - lK, 0)).getReplacedIndexGame(j, Game(gameJK.lose + lJ, gameJK.win + lJ, gameJK.draw + rJK - wJ - lJ, 0)).getMaxWin(),
                                            )

                    if minProbability > win:
                        win = minProbability

        return win

    def getDualTable(self): # Self
        return Table(tuple(map(lambda team: team.getDualTeam(), self.teams)))

    def __transform(self, index: int): # Self
        return Table(tuple(map(lambda team: team.getDeletedIndexOpponent(index), self.teams[:index] + self.teams[index + 1:])))


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

print(json.dumps(sorted(response, key = lambda x: x['now'], reverse = True)))
