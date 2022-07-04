
"""
牌形を全パターン舐めるアルゴリズム(通称: 牌くるくる)

牌形を渡された時、先頭が 0 かどうかで処理を変える。
A: 先頭が 0 の時
    先頭から見ていき、初めて 0 でない数字を見つける。
    その場所の数字を 1 引いて、その前の場所の数字を 1 とする。
        例: [0, 0, 0, 3, 2]
            -> [0. 0. 1, 2, 2]
            -> [0. 1. 0, 2, 2]
            -> [1. 0. 0, 2, 2]
B: 先頭が 0 でない時
    先頭よりも後で 0 でない数字を見つける。
    見つけられなかった時は、末尾の数字を先頭の数字に、先頭の数字を 0 にして処理終了。
    見つけれれた場合、先頭の数字を控えておき 0 にする。
    見つかったその場所の数字を 1 引き、その前の場所の数字を先頭の数字 + 1 とする。
        例: [1, 0, 0, 2, 2]
            -> [0. 0. 2, 1, 2]

牌くるくるの動きの例
[0, 0, 4]
[0, 1, 3]
[1, 0, 3]
[0, 2, 2]
[1, 1, 2]
[2, 0, 2]
[0, 3, 1]
[1, 2, 1]
[2, 1, 1]
[3, 0, 1]
[0, 4, 0]
[1, 3, 0]
[2, 2, 0]
[3, 1, 0]
[4, 0, 0]
[0, 0, 4]
"""


def nextHand(hand: list[int]) -> list[int]:
    """
    次の牌形を取得する

    Args:
        hand (list[int]): 牌形

    Returns:
        list[int]: 次の牌形
    """

    # 牌形の先頭が 0 かどうかで処理が分かれる
    if hand[0] != 0:
        return nextHandNonZeroFirst(hand)
    else:
        return nextHandZeroFirst(hand)


def nextHandNonZeroFirst(hand: list[int]) -> list[int]:
    """
    牌形の先頭が 0 でない時の処理

    Args:
        hand (list[int]): 牌形

    Returns:
        list[int]: 次の牌形
    """

    handLength: int = len(hand)
    index = 1

    # 先頭の数字を控えておく
    first = hand[0]
    # どの処理でも先頭は 0 になる
    hand[0] = 0

    while index < handLength:
        # 0 でない数字を見つけた時
        if hand[index] != 0:
            # その場所の数字を 0 にする
            hand[index] -= 1
            # その前の場所の数字を先頭 + 1 の数字にする
            hand[index - 1] = first + 1
            return hand
        index += 1

    # 先頭以外で 0 が見つからなかった時は末尾を先頭の数字にする
    hand[handLength - 1] = first
    return hand

def nextHandZeroFirst(hand: list[int]) -> list[int]:
    """
    牌形の先頭が 0 である時の処理

    Args:
        hand (list[int]): 牌形

    Returns:
        list[int]: 次の牌形
    """

    handLength: int = len(hand)
    index: int = 0

    while index < handLength:
        # 初めて 0 でない数字を見つけた時
        if hand[index] != 0:
            # その場所の数字を 1 引く
            hand[index] -= 1
            # その前の場所を 1 にする
            hand[index - 1] = 1
            return hand
        index += 1

    # ここに来ることはない
    return hand

if __name__ == '__main__':
    assert nextHand([0, 1]) == [1, 0]
    assert nextHand([5, 0, 0, 1]) == [0, 0, 6, 0]
    assert nextHand([0, 0, 3, 1]) == [0, 1, 2, 1]
    assert nextHand([0, 1, 2, 1]) == [1, 0, 2, 1]
    assert nextHand([5, 0, 0, 0]) == [0, 0, 0, 5]

    def countPattern(num: int) -> int:
        count: int = 0
        hand = [0, 0, 0, 0, 0, 0, 0, 0, num]
        while True:
            if len(list(filter(lambda x: x > 4, hand))) == 0:
                count += 1
            hand = nextHand(hand)
            if (hand == [0, 0, 0, 0, 0, 0, 0, 0, num]):
                break
        return count

    assert countPattern(1) == 9
    assert countPattern(2) == 45
    assert countPattern(4) == 495
    assert countPattern(5) == 1278
    assert countPattern(7) == 6030
    assert countPattern(8) == 11385
    assert countPattern(10) == 32211
    assert countPattern(11) == 48879
    assert countPattern(13) == 93600


