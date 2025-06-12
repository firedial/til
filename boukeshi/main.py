from dataclasses import dataclass
import random


INIT_LIST_LENGTH = 2
INIT_GROUP_MIN = 6
INIT_GROUP_MAX = 10

class InputError(Exception):
    pass

@dataclass(frozen=True)
class Group:
    count: int

    def __init__(self, count: int) -> None:
        if count <= 0:
            raise ValueError("Non positive number.")

        object.__setattr__(self, "count", count)

    def __str__(self) -> str:
        return str(self.count)

class Game:
    groups: list[Group]

    def __init__(self) -> None:
        groups = []
        for _ in range(INIT_LIST_LENGTH):
            groups.append(Group(random.randint(INIT_GROUP_MIN, INIT_GROUP_MAX)))

        self.groups = groups

    def play(self, before: int, afterA: int, afterB: int) -> None:
        if before < 1 or afterA < 0 or afterB < 0 or before <= afterA + afterB:
            raise InputError(f"Value is wrong.")

        for index, group in enumerate(self.groups):
            if group.count == before:
                del self.groups[index]
                break
        else:
            raise InputError(f"No exist {before}.")

        if afterA > 0:
            self.groups.append(Group(afterA))
        if afterB > 0:
            self.groups.append(Group(afterB))

    def evaluete(self) -> int:
        e = 0
        for group in self.groups:
            e ^= group.count

        return e

    def getBestStrategy(self) -> (int, int, int):
        x = self.evaluete()
        n = x.bit_length() - 1

        if x == 0:
            target = self.groups[random.randint(0, len(self.groups) - 1)].count
            afterA = random.randint(0, target - 1)
            afterB = random.randint(0, target - afterA - 1)
            return target, afterA, afterB

        target = 0
        for group in self.groups:
            if group.count & 2 ** n != 0:
                target = group.count
                break
        else:
            raise ValueError(f"No exist.")

        return target, target - 2 ** n, x - 2 ** n

    def isWin(self) -> bool:
        return len(self.groups) == 0

    def __str__(self) -> str:
        return str(list(map(lambda x: str(x), self.groups)))

game = Game()

print(game)
print("Are you first move? [y/n]: ")
move = input()
if move == "y":
    turn = 0
elif move == "n":
    turn = 1
else:
    exit()

while True:

    # 挑戦者のターン
    if turn == 0:
        if game.evaluete() == 0:
            print("----- player turn (YOU LOSE) -----")
        else:
            print("----- player turn -----")

        print(game)
        try:
            before, afterA, afterB = map(int, input().split())
        except:
            print("input error!")
            continue

        if before == -1:
            break

        try:
            game.play(before, afterA, afterB)
        except InputError:
            print("input error!")
            continue
        turn = 1

        if game.isWin():
            print("you win")
            break

    # 必勝法を使ってくるコンピュータのターン
    elif turn == 1:
        print("----- computer turn -----")
        print(game)

        before, afterA, afterB = game.getBestStrategy()
        print(str(before) + " " + str(afterA) + " " + str(afterB))

        game.play(before, afterA, afterB)
        turn = 0

        if game.isWin():
            print("computer win")
            break
    else:
        raise ValueError(f"Something wrong.")

