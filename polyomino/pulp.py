import functools
import operator
import polyominoList
import random
import copy

EMPTY_CELL = -1
FILL_CELL = 0


def countFillFullPattern(field: list[int], polyominos: list[list[list[int]]]):
    if len(polyominos) == 0:
        return 1

    count = 0
    polyomino = polyominos.pop()
    for place in polyomino:
        for cell in place:
            if field[cell] != EMPTY_CELL:
                break
        else:
            for cell in place:
                field[cell] = FILL_CELL
            count += countFillFullPattern(field, polyominos)
            for cell in place:
                field[cell] = EMPTY_CELL

    polyominos.append(polyomino)
    return count


def getFillFullPattern(field: list[int], polyominos: list[list[list[int]]], number, answer):
    if len(polyominos) == 0:
        answer.append(field.copy())
        return 1

    count = 0
    polyomino = polyominos.pop()
    for place in polyomino:
        for cell in place:
            if field[cell] != EMPTY_CELL:
                break
        else:
            for cell in place:
                field[cell] = number
            count += getFillFullPattern(field, polyominos, number + 1, answer)
            for cell in place:
                field[cell] = EMPTY_CELL

    polyominos.append(polyomino)
    return count


def getIdsList(bools, ids):
    result = [ids.copy()]
    for i, b in enumerate(bools):
        if b:
            tmp = copy.deepcopy(result)
            for row in tmp:
                row[i] *= -1
                result.append(row)

    return result


def main(polyominoData, polyominos, polyominoSet, n, result):
    s = sum(map(lambda x: x["count"], polyominoSet))
    if n * n == s:
        if random.randrange(1000) >= 20000:
            return

        testPolyomino = getIdsList(list(map(lambda x: x["hasMirrored"], polyominoSet)), list(map(lambda x: x["id"], polyominoSet)))

        for ids in testPolyomino:
            testPolyominoSet = list(map(lambda x: polyominoData[x], ids))

            field = [EMPTY_CELL for _ in range(n * n)]
            count = countFillFullPattern(field, testPolyominoSet)

            if count != 0:
                # uniqueCount = functools.reduce(operator.floordiv, map(lambda x: 4 // x["rotate"], testPolyominoSet), count)
                result[frozenset(ids)] = count // 4

        return

    if n * n < s or len(polyominos) == 0:
        return

    p = polyominos.pop()
    polyominoSet.append(p)
    main(polyominoData, polyominos, polyominoSet, n, result)

    polyominoSet.pop()
    main(polyominoData, polyominos, polyominoSet, n, result)
    polyominos.append(p)


def getPossiblePlace(n, polyomino):
    result = []
    for i in range(n):
        for j in range(n):
            for d in range(4):
                place = []
                for dx, dy in polyomino["form"]:
                    if d == 1:
                        dx, dy = -dy, dx
                    if d == 2:
                        dx, dy = -dx, -dy
                    if d == 3:
                        dx, dy = dy, -dx

                    if not (0 <= (i + dx) < n):
                        break
                    if not (0 <= (j + dy) < n):
                        break

                    place.append((i + dx) * n + (j + dy))
                else:
                    result.append(place)

    return result


n = 5
polyominos = polyominoList.getPolyominos()
polyominoData = dict(map(lambda x: (x[0], x[1].setdefault("place", getPossiblePlace(n, x[1]))), polyominos.items()))
usePolyominos = dict(filter(lambda x: x[1]["rotate"] == 4 and x[1]["id"] > 0, polyominos.items()))

result = {}
main(polyominoData, list(usePolyominos.values()), [], n, result)

print(result)

minResult = list(filter(lambda x: x[1] == 2, result.items()))
pieceCountMax = 0
for r in minResult:
    f = [EMPTY_CELL for _ in range(n * n)]
    answer = []
    getFillFullPattern(f, list(map(lambda x: polyominoData[x], r[0])), 1, answer)
    pieceCount = len(r[0])
    pieceCountMax = pieceCount if pieceCountMax < pieceCount else pieceCountMax

    print("-" * 50)
    print("[%d] pattern %d" % (pieceCount, r[1]))
    # print(list(map(lambda x: polyominos[x], r[0])))

    for a in answer:
        if max(a[0], a[n - 1], a[n * n - n], a[-1]) != a[0]:
            continue

        print("-" * 10)
        for i, cell in enumerate(a):
            if i % n == 0:
                print()
            print("%3d" % cell, end="")
        print()


print("-" * 50)
print(pieceCountMax)


# answer = []
# for k, v in result.items():
#     count = functools.reduce(operator.floordiv, map(lambda y: 4 // polyominoRoutate[y], k), v)
#     if count == 4:
#         answer.append(k)
#
# print(result)
# print(answer)
