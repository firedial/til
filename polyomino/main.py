import functools
import operator
import polyominoList
import random
import copy

EMPTY_CELL = 0


def deletePolyomino(f, p, x, y, d):
    for dx, dy in p:
        if d == 1:
            dx, dy = -dy, dx
        if d == 2:
            dx, dy = -dx, -dy
        if d == 3:
            dx, dy = dy, -dx

        f[x + dx][y + dy] = EMPTY_CELL


def putPolyomino(f, n, p, pn, x, y, d) -> bool:
    """
    d = 0
        そのまま
    d = 1
        左90度

    """
    for dx, dy in p:
        if d == 1:
            dx, dy = -dy, dx
        if d == 2:
            dx, dy = -dx, -dy
        if d == 3:
            dx, dy = dy, -dx

        if not (0 <= (x + dx) < n):
            return False
        if not (0 <= (y + dy) < n):
            return False

        if f[x + dx][y + dy] != EMPTY_CELL:
            return False

    for dx, dy in p:
        if d == 1:
            dx, dy = -dy, dx
        if d == 2:
            dx, dy = -dx, -dy
        if d == 3:
            dx, dy = dy, -dx

        f[x + dx][y + dy] = pn

    return True


def countFullPolyominoSet(field, n, polyominos) -> int:
    if len(polyominos) == 0:
        return 1

    count = 0
    polyomino = polyominos.pop()
    for i in range(n):
        for j in range(n):
            if f[i][j] != EMPTY_CELL:
                continue

            for d in range(4):
                if not putPolyomino(field, n, polyomino["form"], polyomino["id"], i, j, d):
                    continue

                count += countFullPolyominoSet(field, n, polyominos)
                deletePolyomino(field, polyomino["form"], i, j, d)

    polyominos.append(polyomino)
    return count


def getFullPolyominoSet(field, n, polyominos, answer):
    if len(polyominos) == 0:
        answer.append(copy.deepcopy(field))
        return True

    polyomino = polyominos.pop()
    for i in range(n):
        for j in range(n):
            if f[i][j] != EMPTY_CELL:
                continue

            for d in range(4):
                if not putPolyomino(field, n, polyomino["form"], polyomino["id"], i, j, d):
                    continue

                getFullPolyominoSet(field, n, polyominos, answer)

                deletePolyomino(field, polyomino["form"], i, j, d)

    polyominos.append(polyomino)
    return False


def getIdsList(bools, ids):
    result = [ids.copy()]
    for i, b in enumerate(bools):
        if b:
            tmp = copy.deepcopy(result)
            for row in tmp:
                row[i] *= -1
                result.append(row)

    return result


def main(polyominos_hoge, polyominos, polyominoSet, n, result):
    s = sum(map(lambda x: x["count"], polyominoSet))
    if n * n == s:
        if random.randrange(1000) >= 20000:
            return

        testPolyomino = getIdsList(list(map(lambda x: x["hasMirrored"], polyominoSet)), list(map(lambda x: x["id"], polyominoSet)))

        for ids in testPolyomino:
            testPolyominoSet = list(map(lambda x: polyominos_hoge[x], ids))

            field = [[EMPTY_CELL for _ in range(n)] for _ in range(n)]
            count = countFullPolyominoSet(field, n, testPolyominoSet)
            if count != 0:
                uniqueCount = functools.reduce(operator.floordiv, map(lambda x: 4 // x["rotate"], testPolyominoSet), count)
                result[frozenset(map(lambda x: x["id"], testPolyominoSet))] = uniqueCount // 4

        return

    if n * n < s or len(polyominos) == 0:
        return

    p = polyominos.pop()
    polyominoSet.append(p)
    main(polyominos_hoge, polyominos, polyominoSet, n, result)

    polyominoSet.pop()
    main(polyominos_hoge, polyominos, polyominoSet, n, result)
    polyominos.append(p)


n = 6
f = [[EMPTY_CELL for _ in range(n)] for _ in range(n)]
polyominos = polyominoList.getPolyominos()

# r = countFullPolyominoSet(f, n, [polyominos[0], polyominos[6], polyominos[10]])

result = {}
usePolyominos = list(filter(lambda x: x["rotate"] == 4 and x["id"] > 0, polyominoList.getPolyominos().values()))
# usePolyominos = list(filter(lambda x: x["id"] == 20 or x["id"] == 17 or x["id"] == 13 or x["id"] == 21 or x["id"] == 18, polyominoList.getPolyominos().values()))
main(polyominoList.getPolyominos(), usePolyominos, [], n, result)
minResult = list(filter(lambda x: x[1] == 2, result.items()))

pieceCountMax = 0
for r in minResult:
    f = [[EMPTY_CELL for _ in range(n)] for _ in range(n)]
    answer = []
    getFullPolyominoSet(f, n, list(map(lambda x: polyominos[x], r[0])), answer)
    pieceCount = len(r[0])
    pieceCountMax = pieceCount if pieceCountMax < pieceCount else pieceCountMax

    print("-" * 50)
    print("[%d] pattern %d" % (pieceCount, r[1]))
    print(list(map(lambda x: polyominos[x], r[0])))

    for a in answer:
        if max(a[0][0], a[0][-1], a[-1][0], a[-1][-1]) != a[0][0]:
            continue

        print("-" * 10)
        for row in a:
            for cell in row:
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
