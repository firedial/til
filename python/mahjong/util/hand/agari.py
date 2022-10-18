from . import remove


def isAgari(hand: list[int]) -> bool:
    """
    渡された牌形が和了形であるかどうかを判定する

    牌の枚数によって判定条件が変わる
        3n + 2 枚のとき: 1 雀頭 n 面子のときに限り和了形
        3n + 1 枚のとき: 和了形にならない
        3n 枚のとき: n 面子のときに限り和了形

    Args:
        hand (list[int]): 牌形

    Returns:
        bool: 和了形であれば True / そうでないとき False

    """
    # 牌の枚数が全部 0 なら和了形
    if len(list(filter(lambda x: x != 0, hand))) == 0:
        return True

    # 牌の枚数が一つでも 0 未満なら和了形ではない
    if len(list(filter(lambda x: x < 0, hand))) > 0:
        return False

    # 牌の合計枚数
    count: int = sum(hand)

    # 枚数が 3n + 1 場合は和了形にならない
    if count % 3 == 1:
        return False

    # 枚数が 3n + 2 場合は頭を除去する
    if count % 3 == 2:
        for h in remove.removedTilesPossible(hand, [2]):
            if isAgari(h):
                return True
        else:
            return False

    # 3n 枚の時のは面子の除去
    for h in remove.removedTilesListPossible(hand, [[3], [1, 1, 1]]):
        if isAgari(h):
            return True
    else:
        return False


def isSevenPairs(hand: list[int]) -> bool:
    """
    七対子かどうかを判定する

    Args:
        hand: (list[int]): 牌形

    Returns:
        bool: 七対子形なら True / そうでない時 False
    """
    return len(list(filter(lambda x: x == 2, hand))) == 7


if __name__ == "__main__":
    assert isAgari([3, 1, 1, 1, 1, 1, 1, 1, 4])
    assert isAgari([3, 1, 1, 1, 1, 1, 1, 2, 3])
    assert isAgari([3, 1, 1, 1, 1, 1, 2, 1, 3])
    assert isAgari([3, 1, 1, 1, 1, 2, 1, 1, 3])
    assert isAgari([3, 1, 1, 1, 2, 1, 1, 1, 3])
    assert isAgari([3, 1, 1, 2, 1, 1, 1, 1, 3])
    assert isAgari([3, 1, 2, 1, 1, 1, 1, 1, 3])
    assert isAgari([3, 2, 1, 1, 1, 1, 1, 1, 3])
    assert isAgari([4, 1, 1, 1, 1, 1, 1, 1, 3])

    assert isAgari([])
    assert not isAgari([1])
    assert isAgari([2])
    assert isAgari([3])
    assert not isAgari([4])

    assert isAgari([2, 3, 3])
    assert isAgari([2, 3, 1, 1, 1])
    assert isAgari([1, 1, 3, 1, 1, 1])

    assert not isSevenPairs([1, 1, 3, 1, 1, 1])
    assert not isSevenPairs([2, 2, 0, 2, 0])
    assert isSevenPairs([2, 2, 0, 2, 2, 0, 2, 2, 2])
