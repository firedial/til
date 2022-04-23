
import wait
import remove
import agari

def extendHai(hai):
    hai_ = hai.copy()
    hai_.insert(0, 0)
    hai_.append(0)
    return hai_

def isMentsuIrreducible(hai):
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
            return False
    else:
        return True

def isAtamaIrreducible(hai):
    countWaitingHai = wait.countWaitingHai(hai)

    for hai_ in remove.removedAtamaPattern(hai):
        count = wait.countWaitingHai(hai_)
        
        # 除去した牌形が和了形なら除去した方に和了牌があるので +1 する
        if agari.isAgari(hai_):
            count += 1

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
        if not isAtamaIrreducible(h):
            return False

    return True

if __name__ == '__main__':
    print(isMentsuIrreducible([3, 1, 1, 0, 0, 2]))
    print(isAtamaIrreducible([3, 1, 1]))
    print(isIrreducible([1, 1, 1, 1, 1]))

