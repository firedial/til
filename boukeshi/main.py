from dataclasses import dataclass
import random
import sys


# 入力エラーの例外
class InputError(Exception):
    pass

# グループの本数を管理するクラス
@dataclass(frozen=True)
class Group:
    count: int

    def __init__(self, count: int) -> None:
        if count <= 0:
            raise ValueError("Non positive number.")

        object.__setattr__(self, "count", count)

    def __str__(self) -> str:
        return str(self.count)

# ゲーム状態を管理するクラス
class Game:
    groups: list[Group]

    def __init__(self, groupCount: int, minCount: int, maxCount: int) -> None:
        """
        Args:
            groupCount int: グループの数
            minCount int: 各グループの最小本数
            maxCount int: 各グループの最大本数
        """

        if groupCount <= 0 or minCount <= 0 or maxCount <= 0:
            raise ValueError("Game init args are wrong.")

        # ランダムに盤面を作成する
        groups = []
        for _ in range(groupCount):
            groups.append(Group(random.randint(minCount, maxCount)))

        self.groups = groups

    # プレイを実行する
    def play(self, before: int, afterA: int, afterB: int) -> None:
        """
        Args:
            before int: 削除対象のグループの本数
            afterA int: 新規にできるグループの本数
            afterB int: 新規にできるグループの本数
        """

        # 入力値が不正の時
        if before < 1 or afterA < 0 or afterB < 0 or before <= afterA + afterB:
            raise InputError(f"Value is wrong.")

        # 削除対象グループの探索
        for index, group in enumerate(self.groups):
            if group.count == before:
                # 削除対象グループの削除
                del self.groups[index]
                break
        else:
            # 削除対象グループが鳴ければ例外を出す
            raise InputError(f"No exist {before}.")

        # 新規にできたグループの追加
        if afterA > 0:
            self.groups.append(Group(afterA))
        if afterB > 0:
            self.groups.append(Group(afterB))

    # 評価値の計算
    def evaluete(self) -> int:
        e = 0
        for group in self.groups:
            e ^= group.count

        return e

    # 勝敗判定
    def isWin(self) -> bool:
        return len(self.groups) == 0

    def __str__(self) -> str:
        return str(list(map(lambda x: str(x), self.groups)))

# 必勝法通りプレイする関数
def getBestStrategy(game: Game) -> (int, int, int):
    x = game.evaluete()
    n = x.bit_length() - 1

    # 必勝盤面でないときはランダムで棒を消す
    if x == 0:
        target = game.groups[random.randint(0, len(game.groups) - 1)].count
        afterA = random.randint(0, target - 1)
        afterB = random.randint(0, target - afterA - 1)
        return target, afterA, afterB

    # 必勝法通り棒を消す
    target = 0
    for group in game.groups:
        if group.count & 2 ** n != 0:
            target = group.count
            break
    else:
        raise ValueError(f"No exist.")

    return target, target - 2 ** n, x - 2 ** n

def main(game: Game):
    print(game)

    # 手番の決定
    print("Are you first move? [y/n]: ")
    move = input()
    if move == "y":
        turn = 0
    elif move == "n":
        turn = 1
    else:
        exit()

    # ゲームの実行
    while True:
        # 挑戦者のターン
        if turn == 0:
            if game.evaluete() == 0:
                # 負けが決まっているときのメッセージ
                print("----- player turn (YOU LOSE!!!) -----")
            else:
                print("----- player turn -----")

            print(game)
            try:
                before, afterA, afterB = map(int, input().split())
            except KeyboardInterrupt:
                break
            except:
                print("input error!")
                continue

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

            before, afterA, afterB = getBestStrategy(game)
            print(str(before) + " " + str(afterA) + " " + str(afterB))

            game.play(before, afterA, afterB)
            turn = 0

            if game.isWin():
                print("computer win")
                break

        else:
            raise ValueError(f"Something wrong.")


# ゲーム盤面の作成
args = sys.argv
game = Game(
    int(args[1]), # グループの数
    int(args[2]), # 各グループの最小本数
    int(args[3]), # 各グループの最大本数
)

# ゲーム開始
main(game)
