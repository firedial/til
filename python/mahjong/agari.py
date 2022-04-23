from typing import List
import remove


# 渡された牌形が和了形であるかどうかを判定する
# 牌の枚数が 3n + 2 か 3n 枚のときが対象
def isAgari(hai: List[int]) -> bool:
    # 牌の枚数が全部 0 なら和了形
    if len(list(filter(lambda x: x != 0, hai))) == 0:
        return True

    # 牌の枚数が一つでも 0 未満なら和了形ではない
    if len(list(filter(lambda x: x < 0, hai))) > 0:
        return False

    # 牌の合計枚数
    count: int = sum(hai)

    # 枚数が 3n + 1 場合は和了形にならない
    if count % 3 == 1:
        return False
    
    # 枚数が 3n + 2 場合は頭を除去する
    if count % 3 == 2:
        for hai_ in remove.removedAtamaPattern(hai):
            if isAgari(hai_):
                return True
        else:
            return False

        
    # 3n 枚の時のは面子の除去
    for hai_ in remove.removedMentsuPattern(hai):
        if isAgari(hai_):
            return True
    else:
        return False


def isSevenPairs(hai):
    return len(list(filter(lambda x: x == 2, hai))) == 7

if __name__ == '__main__':
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


    
