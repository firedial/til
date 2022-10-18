from . import agari

MAX_HAI_NUMBER = 4


def getWaitingHai(hand: list[int]) -> list[bool]:
    """
    待ち牌のリストを求める

    Args:
        hand (list[int]): 牌形

    Returns:
        list[bool]: 和了牌なら True / それ以外 False のリスト
    """
    handLength: int = len(hand)
    waitingHai: list[bool] = []

    # 各牌に対して一枚ずつ増やして和了かどうか確認していく
    for index in range(0, handLength):
        # 存在する牌の枚数以上持っていた場合は和了牌とならない
        if hand[index] >= MAX_HAI_NUMBER:
            waitingHai.append(False)
            continue

        hand_ = hand[:]
        hand_[index] += 1
        waitingHai.append(agari.isAgari(hand_))

    return waitingHai


def countWaitingHai(hand: list[int]) -> int:
    """
    待ち牌の種類数を求める

    Args:
        hand (list[int]): 牌形

    Returns:
        int: 待ち牌の種類数
    """
    return len(list(filter(lambda x: x, getWaitingHai(hand))))


if __name__ == "__main__":
    assert getWaitingHai([3, 1, 1, 1, 1, 1, 1, 1, 3]) == [True, True, True, True, True, True, True, True, True]
    assert countWaitingHai([1, 1, 1, 1, 1, 1, 1]) == 3
    assert countWaitingHai([3, 1, 1, 1, 1, 1, 1, 1, 3]) == 9
    assert getWaitingHai([0, 4, 4, 2, 0, 0, 0, 0, 0]) == [True, False, False, True, True, False, False, False, False]
