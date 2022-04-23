
import agari
import haiLoop
import form
import shanten
import irreducible

# print(agari.isAgari([3, 1, 1, 1, 1, 1, 1, 1, 4]))
# print(agari.isSevenPairs([2, 2, 2, 2, 2, 2, 2, 2]))


count = 0
num = 7 

hai = [0, 0, 0, 0, 0, 0, 0, 0, num]
while True:
    # if (not form.isOverFour(hai)) and shanten.isTempai(hai):
    if (not form.isOverFour(hai)
            and form.isNormalForm(hai)
            and shanten.isTempai(hai)
            and irreducible.isIrreducible(hai)):
        for h in hai:
            print(h, end = '')
        print()
        count += 1
    hai = haiLoop.nextHai(hai)
    if (hai == [0, 0, 0, 0, 0, 0, 0, 0, num]):
        break

print(count)

