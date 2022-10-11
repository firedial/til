from HandUtil import HandUtil

import handLoop


def loopHand(hands, num: int):
    handUtil = HandUtil()
    hand = [0, 0, 0, 0, 0, 0, 0, 0, num]
    while True:
        handUtil.setHand(hand)
        if handUtil.isNeedIrreducible():
            hands[handUtil.getHandNumber()] = handUtil.printHandDetail()

            # 雀頭接続順子も考える
            if handUtil.hasAtamaConnectedShuntsu():
                handUtil.setHand(hand, True)
                hands[handUtil.getHandNumber()] = handUtil.printHandDetail()

        hand = handLoop.nextHand(hand)
        if hand == [0, 0, 0, 0, 0, 0, 0, 0, num]:
            break


numbers = [1, 2, 4, 5, 7, 8, 10, 11, 13]
# numbers = [1, 2, 4, 5, 7]
hands = {}

fp = open("list.txt", "w")

for n in numbers:
    loopHand(hands, n)

hands = dict(sorted(hands.items()))
waitingNumber = 1
beforeNumber = 0
for h in hands:
    wait = "W" + str(waitingNumber).zfill(3)
    currentNumber = h // 5

    # 左接地
    if h % 5 == 1:
        wait += "-l"
    # 右接地
    elif h % 5 == 2:
        if beforeNumber == currentNumber:
            waitingNumber -= 1
        wait += "-r"
    else:
        wait += "  "

    waitingNumber += 1

    fp.write(wait + hands[h])
    fp.write("\n")

    beforeNumber = currentNumber

fp.close()
