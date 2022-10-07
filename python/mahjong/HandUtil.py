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

    def getLeftAttachHand(self) -> list[int]:
        if self.hand[0] != 0:
            return self.hand.copy()

        return self.hand[1:] + [0]

    def printHandDetail(self):
        hand = self.hand

        # 牌の全体の枚数
        handCount = sum(hand)

        # 非正規系の場合は正規系にした際の枚数
        # 雀頭接続順子の場合は追加で 3 足す
        normalHandCount = handCount + (2 if handCount % 3 == 2 else 0) + (3 if self.isConnected else 0)

        waiting = wait.getWaitingHai(hand)
        hasAtamaWaiting = handCount % 3 == 2 and self.isAgari()

        waitingKindCount = len(list(filter(lambda x: x, waiting)))
        waitingCount = sum([4 - h if w else 0 for (h, w) in zip(hand, waiting)])

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
        leftAttachedHandString = ",".join(map(lambda x: str(x), self.getLeftAttachHand()))
        waitingString = ",".join(map(lambda x: "1" if x else "0", waiting))

        print(
            "|%2s|%2s|%s||%s|%s|%s||%s|%s|%s|"
            % (
                handCount,
                normalHandCount,
                handLength,
                "-" if isLeftIrreducible is None else ("o" if isLeftIrreducible else "x"),
                "-" if isRightIrreducible is None else ("o" if isRightIrreducible else "x"),
                "o" if handLength != 8 else ("x" if isLeftIrreducible == True else "o"),
                handString,
                leftAttachedHandString,
                waitingString,
            )
        )


if __name__ == "__main__":
    h = HandUtil()
    h.setHand([3, 3])
    assert h.isValid()

    h.setHand([2, 2, 5])
    assert not h.isValid()

    h.setHand([2, -1, 4])
    assert not h.isValid()
