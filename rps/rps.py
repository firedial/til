
n = 7

def isLose(a: int, b: int) -> bool:
    return not ((n + a - b) % n <= n // 2)

def isDraw(a: int, b: int) -> bool:
    return a == b

def isWin(a: int, b: int) -> bool:
    return not isLose(a, b) and not isDraw(a, b)

def getWeightLose(a: int, b: int) -> int:
    diff = a - b
    if diff > n // 2:
        return diff - n
    if diff < -1 * (n // 2):
        return diff + n
    return diff

def getWin(hands: list[int]) -> int:
    result = {i: 0 for i in range(n)}
    for i in hands:
        for j in hands:
            result[i] += getWeightLose(i, j)

    maxNumber = 0
    for number in result.values():
        if number > maxNumber:
            maxNumber = number

    maxIndex = None
    for index, number in result.items():
        if number == maxNumber:
            if maxIndex is not None:
                raise Exception("wrong")
            maxIndex = index

    return maxIndex

def getHandsFromNumber(number: int) -> list[int]:
    hand = 0
    hands = []
    while True:
        if number == 0:
            break

        if number % 2 == 1:
            hands.append(hand)

        hand += 1
        number //= 2

    return hands

for k in range(2 ** n):
    hands = getHandsFromNumber(k)
    if len(hands) == 0:
        continue
    if len(hands) == 1:
        continue
    if len(hands) == n:
        continue

    getWin(hands)

for i in range(n):
    for j in range(n):
        if isDraw(i, j) or isLose(i, j) == isWin(j, i):
            # print(getWeightLose(i, j))
            pass
            # print(isWin(i, j))
        else:
            print("wrong")



