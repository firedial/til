
import sys

import agari
import handLoop
import form
import shanten
import irreducible

# print(agari.isAgari([3, 1, 1, 1, 1, 1, 1, 1, 4]))
# print(agari.isSevenPairs([2, 2, 2, 2, 2, 2, 2, 2]))


count = 0
num = int(sys.argv[1])

hai = [0, 0, 0, 0, 0, 0, 0, 0, num]

hai = [0, 0, 0, 0, 0, 0, 0, 0, num]
while True:
    # if (not form.isOverFour(hai)) and shanten.isTempai(hai):
    if (not form.isOverFour(hai)
            and form.isBasicForm(hai)
            and shanten.isTempai(hai)
            # and irreducibleStructure.isIrreducible(hai)):
            and irreducible.isIrreducible(hai)):
        print(hai)
        count += 1
    hai = handLoop.nextHand(hai)
    if (hai == [0, 0, 0, 0, 0, 0, 0, 0, num]):
        break

print(count)


