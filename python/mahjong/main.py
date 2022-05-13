
import sys

import agari
import haiLoop
import form
import shanten
import irreducible
import irreducibleStructure
import waitStructure
import yaku

# print(agari.isAgari([3, 1, 1, 1, 1, 1, 1, 1, 4]))
# print(agari.isSevenPairs([2, 2, 2, 2, 2, 2, 2, 2]))


count = 0
num = int(sys.argv[1])

yakuCount = set()
yakuTwoCount = []

hai = [0, 0, 0, 0, 0, 0, 0, 0, num]
while True:
    if (not form.isOverFour(hai)
            and agari.isAgari(hai)):
        count += 1
        for index in range(9):
            if hai[index] != 0:
                yakus = yaku.getAll(hai, index + 1, True, True)
                if len(yakus) == 1:
                    yakuCount.add(yakus[0])
                elif (set(yakus) != {1050, 1058}) and (set(yakus) != {1062, 1054}):
                    yakuTwoCount.append(yakus)

    hai = haiLoop.nextHai(hai)
    if (hai == [0, 0, 0, 0, 0, 0, 0, 0, num]):
        break


yakuList = list(map(yaku.transNumToYaku, list(yakuCount)))
for y in yakuList:
    print(y)

print(yakuTwoCount)
print(count)

# hai = [0, 0, 0, 0, 0, 0, 0, 0, num]
# while True:
#     # if (not form.isOverFour(hai)) and shanten.isTempai(hai):
#     if (not form.isOverFour(hai)
#             and form.isNormalForm(hai)
#             and shanten.isTempai(hai)
#             # and irreducibleStructure.isIrreducible(hai)):
#             and irreducible.isIrreducible(hai)):
#         print(' 0', end = '')
#         for h in hai:
#             print(h, end = '')
#         print('0')
#         waitStructure.printWaitingStructure([0] + hai + [0])
#         count += 1
#     hai = haiLoop.nextHai(hai)
#     if (hai == [0, 0, 0, 0, 0, 0, 0, 0, num]):
#         break
#

