import handLoop
import shanten
import irreducible
import form


def getIrreducibleList(hand: list[int], irreducibleList: list[list[int]]) -> None:
    if irreducible.isIrreducible(hand):
        irreducibleList.append(hand)
        return

    # 牌の合計枚数
    count: int = sum(hand)

    if count % 3 == 1:
        removedHands = irreducible.getAtamaNoChange(hand)
        for removedhand in removedHands:
            getIrreducibleList(removedhand, irreducibleList)

        removedHands = irreducible.getAtamaConnectdShuntsuIrreducible(hand)
        for removedhand in removedHands:
            getIrreducibleList(removedhand, irreducibleList)

    removedHands = irreducible.getMentsuNoChange(hand)
    for removedhand in removedHands:
        getIrreducibleList(removedhand, irreducibleList)


count = 0
# num = int(sys.argv[1])
num = 13

hai = [0, 0, 0, 0, 0, 0, 0, 0, num]
while True:
    if not form.isOverFour(hai) and form.isBasicForm(hai) and shanten.isTempai(hai):
        l = []
        getIrreducibleList(hai, l)
        rl = list(map(list, set(map(tuple, map(lambda x: [2] if x == [3, 1, 1] else x, (map(form.getUniformForm, l)))))))
        rl1 = list(filter(lambda x: sum(x) % 3 == 1, rl))
        rl2 = list(filter(lambda x: sum(x) % 3 == 2, rl))
        if len(rl) != 1 and len(rl1) > 1 and len(rl2) > 1:
            print(hai)
            print(len(rl))
            print(rl)
            count += 1

    hai = handLoop.nextHand(hai)
    if hai == [0, 0, 0, 0, 0, 0, 0, 0, num]:
        break

print(count)
