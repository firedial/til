from util.hand.HandUtil import HandUtil
from util.handImage.makeImage import makeImage

fp = open("list.txt", "w")

handNumbers = []
with open("hands.txt", "r") as f:
    for line in f:
        handNumbers.append(int(line))

handNumbers.sort()

waitingNumber = 1
beforeNumber = 0
handUtil = HandUtil()
for handNumber in handNumbers:
    currentNumber = handNumber // 5

    # 左接地
    if handNumber % 5 == 1:
        wait = "W" + str(waitingNumber).zfill(3) + "-l"
        blank = ""
    # 右接地
    elif handNumber % 5 == 2:
        if beforeNumber == currentNumber:
            waitingNumber -= 1
        wait = "W" + str(waitingNumber).zfill(3) + "-r"
        blank = ""
    else:
        wait = "W" + str(waitingNumber).zfill(3)
        blank = "  "

    handUtil.setHandByNumber(handNumber)
    fp.write(wait + blank + handUtil.printHandDetail())
    fp.write("\n")
    # print(wait + blank + handUtil.printHandDetail())
    # makeImage.makeImage(wait, handUtil.getHand(), handUtil.getAtamaNumber())
    # makeImage.makeWaitImage(
    #     "Wait_" + wait,
    #     list(map(lambda x: 1 if x else 0, handUtil.getWaitng())),
    #     (1 if handUtil.isAgari() else 0) + (1 if handUtil.getIsConnected() else 0),
    # )
    # print(handUtil.printHandTable(wait))

    waitingNumber += 1
    beforeNumber = currentNumber

fp.close()
