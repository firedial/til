import sys

import agari
import handLoop
import form
import shanten
import irreducible
import wait

# print(agari.isAgari([3, 1, 1, 1, 1, 1, 1, 1, 4]))
# print(agari.isSevenPairs([2, 2, 2, 2, 2, 2, 2, 2]))


count = 0
# num = inut(sys.argv[1])
num = 8

hai = [0, 0, 0, 0, 0, 0, 0, 0, num]
while True:
    # if (not form.isOverFour(hai)) and shanten.isTempai(hai):
    if (
        not form.isOverFour(hai)
        and form.isBasicForm(hai)
        and shanten.isTempai(hai)
        # and irreducibleStructure.isIrreducible(hai)):
        and irreducible.isIrreducible(hai)
    ):
        waitingList = wait.getWaitingHai(hai)
        waitingKindCount = len(list(filter(lambda x: x, waitingList)))
        waitingCount = 0
        for (h, w) in zip(hai, waitingList):
            if w:
                waitingCount += 4 - h

        # 両側の0を省く
        bothAttachHai = form.getUniformForm(hai)
        if len(bothAttachHai) <= 7:
            leftIrreducible = shanten.isTempai(bothAttachHai + [0]) and irreducible.isIrreducible(bothAttachHai + [0])
            rightIrreducible = shanten.isTempai([0] + bothAttachHai) and irreducible.isIrreducible([0] + bothAttachHai)
            print("o" if leftIrreducible else "x", end="")
            print("o" if rightIrreducible else "x", end="|")
        elif len(bothAttachHai) == 8:
            if hai[0] != 0:
                rightIrreducible = shanten.isTempai([0] + bothAttachHai) and irreducible.isIrreducible([0] + bothAttachHai)
                print("-", end="")
                print("o" if rightIrreducible else "x", end="|")
            else:
                leftIrreducible = shanten.isTempai(bothAttachHai + [0]) and irreducible.isIrreducible(bothAttachHai + [0])
                print("o" if leftIrreducible else "x", end="")
                print("-", end="|")

        elif len(bothAttachHai) == 9:
            print("--", end="|")

        print(hai, end="||")
        print(list(map(lambda x: 1 if x else 0, waitingList)), end="||")
        print(waitingKindCount, end="|")
        print(waitingCount)
        count += 1
    hai = handLoop.nextHand(hai)
    if hai == [0, 0, 0, 0, 0, 0, 0, 0, num]:
        break

print(count)
