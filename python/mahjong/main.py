from HandUtil import HandUtil

import handLoop


def loopHand(fp, num: int):
    handUtil = HandUtil()
    hand = [0, 0, 0, 0, 0, 0, 0, 0, num]
    while True:
        handUtil.setHand(hand)
        if handUtil.isNeedIrreducible():
            fp.write(str(handUtil.getHandNumber()))
            fp.write("\n")

            # 雀頭接続順子も考える
            if handUtil.hasAtamaConnectedShuntsu():
                handUtil.setHand(hand, True)
                fp.write(str(handUtil.getHandNumber()))
                fp.write("\n")

        hand = handLoop.nextHand(hand)
        if hand == [0, 0, 0, 0, 0, 0, 0, 0, num]:
            break


numbers = [1, 2, 4, 5, 7, 8, 10, 11, 13]
fp = open("hands.txt", "w")

for n in numbers:
    loopHand(fp, n)

fp.close()
