from enum import Enum

import wait
import remove
import agari


class RemoveHai(Enum):
    MENTSU = 0
    ATAMA = 1
    CONNECTED = 2


def isChangingWaiting(waiting: list[bool], atamaWaitingCount: int, removedWaiting: list[bool], removedAtamaWaitingCount: int) -> bool:
    countWaiting = len(list(filter(lambda x: x, waiting)))
    countRemovedWaiting = len(list(filter(lambda x: x, removedWaiting)))

    # あがり牌に昇格した場合(和了牌だが4枚使いだった場合)は待ちに関係する
    for (a, b) in zip(waiting, removedWaiting):
        if not a and b:
            return True

    # 待ちの種類数が変わっていれば true
    return countWaiting + atamaWaitingCount != countRemovedWaiting + removedAtamaWaitingCount


def isIrreducibleByRemovePattern(hand: list[int], pattern: RemoveHai) -> bool:
    waitingHai = wait.getWaitingHai(hand)

    # 和了系になっていた場合は頭も和了牌となる
    isAtamaWaiting = 1 if agari.isAgari(hand) else 0

    match (pattern):
        case RemoveHai.MENTSU:
            removedHand = remove.removedMentsuPattern(hand)
        case RemoveHai.ATAMA:
            removedHand = remove.removedAtamaPattern(hand)
        case RemoveHai.CONNECTED:
            removedHand = remove.removedAtamaConnectedShuntsuPattern(hand)

    for hai_ in removedHand:
        atamaWaitingCount = 0

        if agari.isAgari(hai_):
            match (pattern):
                case RemoveHai.MENTSU:
                    atamaWaitingCount = 1
                case RemoveHai.ATAMA:
                    atamaWaitingCount = 1
                case RemoveHai.CONNECTED:
                    atamaWaitingCount = 2

        if not isChangingWaiting(waitingHai, isAtamaWaiting, wait.getWaitingHai(hai_), atamaWaitingCount):
            return False
    else:
        return True


def isMentsuIrreducible(hand: list[int]) -> bool:
    return isIrreducibleByRemovePattern(hand, RemoveHai.MENTSU)


def isAtamaIrreducible(hand: list[int]) -> bool:
    return isIrreducibleByRemovePattern(hand, RemoveHai.ATAMA)


def isAtamaConnectedShuntsuIrreducible(hand: list[int]) -> bool:
    return isIrreducibleByRemovePattern(hand, RemoveHai.CONNECTED)


def getAtamaConnectdShuntsuIrreducible(hai) -> list[list[int]]:
    rt = []
    countWaitingHai = wait.countWaitingHai(hai)

    for hai_ in remove.removedAtamaConnectedShuntsuPattern(hai):
        count = wait.countWaitingHai(hai_)

        # 除去した牌形が和了形なら除去した方に和了牌があるので +2 する
        if agari.isAgari(hai_):
            count += 2

        if countWaitingHai == count:
            rt.append(hai_)

    return rt


def getAtamaNoChange(hai) -> list[list[int]]:
    rt = []
    countWaitingHai = wait.countWaitingHai(hai)

    for hai_ in remove.removedAtamaPattern(hai):
        count = wait.countWaitingHai(hai_)

        # 除去した牌形が和了形なら除去した方に和了牌があるので +1 する
        if agari.isAgari(hai_):
            count += 1

        if countWaitingHai == count:
            rt.append(hai_)

    return rt


def getMentsuNoChange(hai) -> list[list[int]]:
    rt = []
    countWaitingHai = wait.countWaitingHai(hai)

    # 和了系になっていた場合は頭の和了牌を含むので +1 する
    if agari.isAgari(hai):
        countWaitingHai += 1

    for hai_ in remove.removedMentsuPattern(hai):
        count = wait.countWaitingHai(hai_)

        # 除去した牌形が和了形なら除去した方に和了牌があるので +1 する
        if agari.isAgari(hai_):
            count += 1

        if countWaitingHai == count:
            rt.append(hai_)

    return rt


def isIrreducible(h):
    if not isMentsuIrreducible(h):
        return False

    # 正規形のときは待ち送り形の既約もみる
    if sum(h) % 3 == 1:
        if not isAtamaIrreducible(h) or not isAtamaConnectedShuntsuIrreducible(h):
            return False

    return True


if __name__ == "__main__":
    assert isMentsuIrreducible([3, 1, 1, 0, 0, 2])
    assert isAtamaIrreducible([3, 1, 1, 0, 0, 1, 1, 3])
    assert not isIrreducible([1, 1, 1, 1, 1])
    assert not isIrreducible([3, 1, 1, 0, 0, 1, 1, 3])
    assert isIrreducible([0, 1, 1, 4, 1, 1, 0, 0])
