
def isOverFour(hand: list[int]) -> bool:
    """
    4 枚以上使っていないか判定する

    Args:
        hand (lsit[int]): 牌形

    Returns:
        bool: 4 枚以上使っていた場合は True / それ以外 False
    """
    return len(list(filter(lambda x: x > 4, hand))) > 0

def isBasicForm(hand: list[int]) -> bool:
    """
    基本形かどうかを判定する

    判定方法:
        1. 後方重心なら基本形ではない
        2. 両端接地/左接地/右接地/無接地 の判定をする
        3. 左右対称形かつ右接地は基本形ではない
        4. 無接地かつ左から 2 以上離れていた場合は基本形ではない
        5. 基本形である

    Args:
        hand (lsit[int]): 牌形

    Returns:
        bool: 基本形であれば True / そうでないとき False
    """

    gravity: int = handGravityPosition(hand)

    # 後方重心なら基本形ではない
    if gravity == -1:
        return False

    # 左右対称形かつ右接地は基本形ではない
    if gravity == 0 and hand[-1] != 0:
        return False

    # 無接地かつ左から 2 以上離れている時は基本形ではない
    if hand[0] == 0 and hand[-1] == 0 and hand[1] == 0:
        return False

    # その他の場合は基本形である
    return True




def handGravityPosition(hand: list[int]) -> int:
    """
    牌形の重心を求める

    両端に接地している連続する 0 を無視する。
    両端から見て行った時、大きい数字がある方に重心がある。
    同じ場合はさらに一つ内側で比較する。最後まで一緒なら左右対称形。

    例:
        [0, 2, 4, 0, 0] -> 後方重心
        [0, 2, 2, 3, 2] -> 後方重心
        [0, 2, 2, 1, 2] -> 前方重心
        [0, 2, 1, 1, 2, 0, 0] -> 左右対称形

    Args:
        hand (list[int]): 牌形

    Returns:
        int: 前方重心 1 / 左右対称 0 / 後方重心 -1

    """
    handLength: int = len(hand)

    first: int = 0
    last: int = handLength - 1

    # 前から見たときに初めて 0 でない場所を見つける
    while first < handLength:
        if hand[first] != 0:
            break
        first += 1

    # 後ろから見たときに初めて 0 でない場所を見つける
    while 0 <= last:
        if hand[last] != 0:
            break
        last -= 1

    # 両端から重心を見ていく
    while first < last:
        if hand[first] > hand[last]:
            # 前方重心
            return 1
        if hand[first] < hand[last]:
            # 後方重心
            return -1
        first += 1
        last -= 1

    # 左右対称形
    return 0
