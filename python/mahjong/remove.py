
def getNonZeroHai(pattern):
    isNonZero = lambda hai: len(list(filter(lambda x: x < 0, hai))) == 0
    return list(filter(isNonZero, pattern))

def formRemovedPattern(hai, form):
    loopCount = len(hai) - len(form) + 1
    pattern = []

    for x in range(0, loopCount):
        hai_ = hai[:]
        for y, value in enumerate(form):
            hai_[x + y] -= value
        pattern.append(hai_)

    return getNonZeroHai(pattern)

def formsRemovedPattern(hai, forms):
    pattern = []

    for form in forms:
        pattern += formRemovedPattern(hai, form)

    return pattern

def removedAtamaPattern(hai):
    """
    刻子のパターンを省けるだけ省いた牌形のリストを返す

    Args:
        hand (list[int]): 牌形

    Returns:
        lits[list[int]]: 牌形から刻子のパターンを省いた牌形のリスト
    """
    return formRemovedPattern(hai, [2])

def removedKotsuPattern(hand: list[int]) -> list[list[int]]:
    """
    刻子のパターンを省けるだけ省いた牌形のリストを返す

    Args:
        hand (list[int]): 牌形

    Returns:
        lits[list[int]]: 牌形から刻子のパターンを省いた牌形のリスト
    """
    return formRemovedPattern(hand, [3])

def removedShuntsuPattern(hand: list[int]) -> list[list[int]]:
    """
    順子のパターンを省けるだけ省いた牌形のリストを返す

    Args:
        hand (list[int]): 牌形

    Returns:
        lits[list[int]]: 牌形から順子のパターンを省いた牌形のリスト
    """
    return formRemovedPattern(hand, [1, 1, 1])

def removedAtamaConnectedShuntsuPattern(hand: list[int]) -> list[list[int]]:
    """
    雀頭接続順子のパターンを省けるだけ省いた牌形のリストを返す

    Args:
        hand (list[int]): 牌形

    Returns:
        lits[list[int]]: 牌形から雀頭接続順子のパターンを省いた牌形のリスト
    """
    return formsRemovedPattern(hand, [[3, 1, 1, 0], [0, 1, 1, 3]])

def removedMentsuPattern(hand: list[int]) -> list[list[int]]:
    """
    面子(刻子と順子)のパターンを省けるだけ省いた牌形のリストを返す

    Args:
        hand (list[int]): 牌形

    Returns:
        lits[list[int]]: 牌形から面子のパターンを省いた牌形のリスト
    """
    return removedKotsuPattern(hand) + removedShuntsuPattern(hand)

def removedSendableForm(hai):
    return removedAtamaPattern(hai) + removedAtamaConnectedShuntsuPattern(hai)


if __name__ == '__main__':
    print(formRemovedPattern([1, 2, 3], [1, 2, 1, 2]))
    print(formsRemovedPattern([1, 2, 3], [[2], [1, 1]]))
    print(removedKotsuPattern([1, 2, 3]))
    print(removedShuntsuPattern([1, 2, 3, 3, 2, 0]))
    print(removedMentsuPattern([1, 2, 3, 3, 2, 0]))

    print(removedAtamaConnectedShuntsuPattern([1, 2, 3, 5, 2, 3]))
    print(removedSendableForm([1, 2, 3, 5, 2, 3]))




