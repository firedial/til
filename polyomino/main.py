import functools
import operator
import polyominoList
import random
import copy

EMPTY_CELL = -1


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


def main(polyominos, polyominoSet, n, result):
    s = sum(map(lambda x: x["count"], polyominoSet))
    if n * n == s:
        if random.randrange(1000) >= 20000:
            return
        field = [[EMPTY_CELL for _ in range(n)] for _ in range(n)]
        count = countFullPolyominoSet(field, n, polyominoSet.copy())
        if count != 0:
            uniqueCount = functools.reduce(operator.floordiv, map(lambda x: 4 // x["rotate"], polyominoSet), count)
            result[frozenset(map(lambda x: x["id"], polyominoSet))] = uniqueCount // 4

        return

    if n * n < s or len(polyominos) == 0:
        return

    p = polyominos.pop()
    polyominoSet.append(p)
    main(polyominos, polyominoSet, n, result)

    polyominoSet.pop()
    main(polyominos, polyominoSet, n, result)
    polyominos.append(p)


n = 4
f = [[EMPTY_CELL for _ in range(n)] for _ in range(n)]
polyominos = polyominoList.getPolyominos()

# r = countFullPolyominoSet(f, n, [polyominos[0], polyominos[6], polyominos[10]])

result = {}
usePolyominos = list(filter(lambda x: x["rotate"] == 4, polyominoList.getPolyominos()))
main(usePolyominos, [], n, result)
minResult = list(filter(lambda x: x[1] == 2, result.items()))

pieceCountMax = 0
for r in minResult:
    f = [[EMPTY_CELL for _ in range(n)] for _ in range(n)]
    answer = []
    getFullPolyominoSet(f, n, list(map(lambda x: polyominos[x - 1], r[0])), answer)
    pieceCount = len(r[0])
    pieceCountMax = pieceCount if pieceCountMax < pieceCount else pieceCountMax

    print("-" * 50)
    print("[%d] pattern %d" % (pieceCount, r[1]))

    for a in answer:
        if max(a[0][0], a[0][-1], a[-1][0], a[-1][-1]) != a[0][0] or max(a[0][-1], a[-1][0], a[-1][-1]) != a[0][-1]:
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
