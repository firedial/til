from HandUtil import HandUtil

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
    # 右接地
    elif handNumber % 5 == 2:
        if beforeNumber == currentNumber:
            waitingNumber -= 1
        wait = "W" + str(waitingNumber).zfill(3) + "-r"
    else:
        wait = "W" + str(waitingNumber).zfill(3) + "  "

    handUtil.setHandByNumber(handNumber)
    print(wait + handUtil.printHandDetail())

    waitingNumber += 1
    beforeNumber = currentNumber
