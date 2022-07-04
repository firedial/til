
import waitStructure as wait
import remove
import agari

def extendHai(hai):
    hai_ = hai.copy()
    hai_.insert(0, 0)
    hai_.append(0)
    return hai_

def isMentsuIrreducible(hai):
    countWaitingHai = wait.countWaitingStructure(hai)

    # 和了系になっていた場合は頭の和了牌を含むので +1 する
    if agari.isAgari(hai):
        countWaitingHai += 1

    for hai_ in remove.removedMentsuPattern(hai):
        count = wait.countWaitingStructure(hai_)

        # 除去した牌形が和了形なら除去した方に和了牌があるので +1 する
        if agari.isAgari(hai_):
            count += 1

        if countWaitingHai == count:
            return False
    else:
        return True

def isAtamaIrreducible(hai):
    countWaitingHai = wait.countWaitingStructure(hai)

    for hai_ in remove.removedAtamaPattern(hai):
        count = wait.countWaitingStructure(hai_)

        # 除去した牌形が和了形なら除去した方に和了牌があるので +1 する
        if agari.isAgari(hai_):
            count += 1

        if countWaitingHai == count:
            return False
    else:
        return True

def isAtamaConnectedShuntsuIrreducible(hai):
    countWaitingHai = wait.countWaitingStructure(hai)

    for hai_ in remove.removedAtamaConnectedShuntsuPattern(hai):
        count = wait.countWaitingStructure(hai_)

        # 除去した牌形が和了形なら除去した方に和了牌があるので +3 する
        if agari.isAgari(hai_):
            count += 3

        if countWaitingHai == count:
            return False
    else:
        return True

def isIrreducible(hai):
    # 両端に架空の牌を付け加える
    h = extendHai(hai)

    if not isMentsuIrreducible(h):
        return False

    # 正規形のときは待ち送り形の既約もみる
    if sum(h) % 3 == 1:
        if not isAtamaIrreducible(h) or not isAtamaConnectedShuntsuIrreducible(h):
            return False

    return True

if __name__ == '__main__':
    print(isMentsuIrreducible([3, 1, 1, 0, 0, 2]))
    print(isAtamaIrreducible([3, 1, 1, 0, 0, 1, 1, 3]))
    print(isIrreducible([1, 1, 1, 1, 1]))
    print(isIrreducible([3, 1, 1, 0, 0, 1, 1, 3]))

