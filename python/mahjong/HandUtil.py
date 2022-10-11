import agari
import shanten
import form
import irreducible
import wait


class HandUtil:
    def __init__(self) -> None:
        self.hand: list[int] = []

    def setHand(self, hand: list[int], isConnected: bool = False) -> None:
        self.hand = hand
        self.isConnected = isConnected

    def setHandByNumber(self, number: int) -> None:
        # 5 進数の数字に変換する
        n = []
        while number != 0:
            n.append(number % 5)
            number //= 5
        n.reverse()

        # 左接地させるかどうか判定
        if n[-1] != 3 and n[-1] != 1:
            # 末尾が 3 でない(長さが 9 でない) または末尾が 1 でない(長さ 8 の左接地でない)
            self.hand = list(map(lambda x: 4 - x, [4] + n[2:10]))
        else:
            self.hand = list(map(lambda x: 4 - x, n[2:11]))

        # 雀頭接続順子
        self.isConnected = n[1] == 0

    def isValid(self) -> bool:
        # 0 枚未満の牌を持っているとき
        if len(list(filter(lambda x: x < 0, self.hand))) > 0:
            return False
        # 5 枚以上使っている場合
        if len(list(filter(lambda x: x > 4, self.hand))) > 0:
            return False

        return True

    def isAgari(self) -> bool:
        return agari.isAgari(self.hand)

    def isTempai(self) -> bool:
        return shanten.isTempai(self.hand)

    def isBasicForm(self) -> bool:
        return form.isBasicForm(self.hand)

    def isIrreducible(self) -> bool:
        return shanten.isTempai(self.hand) and irreducible.isIrreducible(self.hand)

    def isNeedIrreducible(self) -> bool:
        return self.isValid() and self.isBasicForm() and self.isIrreducible()

    def hasAtamaConnectedShuntsu(self) -> bool:
        handCount = sum(self.hand)
        return (handCount == 5 or handCount == 8) and self.isAgari()

    def getLeftAttachHand(self) -> list[int]:
        if self.hand[0] != 0:
            return self.hand.copy()

        return self.hand[1:] + [0]

    def getHandNumber(self) -> int:
        handCount = sum(self.hand)
        handCountMap = {1: 0, 4: 1, 7: 2, 10: 3, 13: 4}

        leftAttachHand = self.getLeftAttachHand()
        normalHandNumber = 2 if handCount % 3 != 2 else (0 if self.isConnected else 1)
        normalHandCount = handCount + (2 if handCount % 3 == 2 else 0) + (3 if self.isConnected else 0)
        place = 0 if leftAttachHand[-1] == 0 and leftAttachHand[-2] == 0 else (3 if leftAttachHand[-1] != 0 else (1 if self.hand[0] != 0 else 2))

        number = 0

        handNumber = [handCountMap[normalHandCount]] + [normalHandNumber] + list(map(lambda x: 4 - x, leftAttachHand)) + [place]

        for hai in handNumber:
            number *= 5
            number += hai

        return number

    def printHandDetail(self) -> str:
        hand = self.hand

        # 牌の全体の枚数
        handCount = sum(hand)

        # 非正規系の場合は正規系にした際の枚数
        # 雀頭接続順子の場合は追加で 3 足す
        normalHandCount = handCount + (2 if handCount % 3 == 2 else 0) + (3 if self.isConnected else 0)

        waiting = wait.getWaitingHai(hand)
        hasAtamaWaiting = handCount % 3 == 2 and self.isAgari()

        waitingKindCount = sum(list(filter(lambda x: x, waiting))) + (0 if not hasAtamaWaiting else (2 if self.isConnected else 1))
        waitingCount = sum([4 - h if w else 0 for (h, w) in zip(hand, waiting)]) + (0 if not hasAtamaWaiting else (5 if self.isConnected else 2))

        # 両側の0を省く
        bothAttachHand = form.getUniformForm(hand)
        handLength = len(bothAttachHand)
        handUtil = HandUtil()
        if len(bothAttachHand) <= 7:
            handUtil.setHand(bothAttachHand + [0])
            isLeftIrreducible = handUtil.isIrreducible()
            handUtil.setHand([0] + bothAttachHand)
            isRightIrreducible = handUtil.isIrreducible()
        elif len(bothAttachHand) == 8:
            # 左接地の時
            if hand[0] != 0:
                handUtil.setHand([0] + bothAttachHand)
                isRightIrreducible = handUtil.isIrreducible()
                isLeftIrreducible = None
            # 右接地の時
            else:
                handUtil.setHand(bothAttachHand + [0])
                isRightIrreducible = None
                isLeftIrreducible = handUtil.isIrreducible()
        else:
            isRightIrreducible = None
            isLeftIrreducible = None

        handString = ",".join(map(lambda x: str(x), hand))
        waitingString = ",".join(map(lambda x: "1" if x else "0", waiting))

        return "|%9s||%2s|%2s|%s||%s|%s|%s||%s|%s||%s||%s|%2s|" % (
            self.getHandNumber(),
            normalHandCount,
            handCount,
            handLength,
            "-" if isLeftIrreducible is None else ("o" if isLeftIrreducible else "x"),
            "-" if isRightIrreducible is None else ("o" if isRightIrreducible else "x"),
            "o" if handLength != 8 else ("x" if isLeftIrreducible else "o"),
            handString,
            waitingString,
            "-" if not hasAtamaWaiting else ("c" if self.isConnected else "a"),
            waitingKindCount,
            waitingCount,
        )


if __name__ == "__main__":
    h = HandUtil()
    h.setHand([3, 3])
    assert h.isValid()

    h.setHand([2, 2, 5])
    assert not h.isValid()

    h.setHand([2, -1, 4])
    assert not h.isValid()

    numbers = []
    # 通常
    h.setHand([0, 1, 1, 1, 1, 0, 0, 0, 0])
    numbers.append(h.getHandNumber())

    # 雀頭関係
    h.setHand([0, 3, 1, 1, 0, 0, 0, 0, 0])
    numbers.append(h.getHandNumber())
    h.setHand([0, 3, 1, 1, 0, 0, 0, 0, 0], True)
    numbers.append(h.getHandNumber())

    # 長さ8関係
    h.setHand([3, 0, 1, 1, 1, 1, 0, 3, 0])
    numbers.append(h.getHandNumber())
    h.setHand([0, 3, 0, 1, 1, 1, 1, 0, 3])
    numbers.append(h.getHandNumber())

    # 長さ9
    h.setHand([3, 1, 1, 1, 1, 1, 1, 1, 3])
    numbers.append(h.getHandNumber())

    for n in numbers:
        h.setHandByNumber(n)
        assert n == h.getHandNumber()
