import itertools
import functools
import operator
import polyominoList

EMPTY_CELL = -1


def deletePolyomino(f, n, p, x, y, d):
    for dx, dy in p:
        if d == 1:
            dx, dy = -dy, dx
        if d == 2:
            dx, dy = -dx, -dy
        if d == 3:
            dx, dy = dy, -dx

        f[x + dx][y + dy] = EMPTY_CELL


def putPolyomino(f, n, p, pn, x, y, d):
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
            return None
        if not (0 <= (y + dy) < n):
            return None

        if f[x + dx][y + dy] != EMPTY_CELL:
            return None

    for dx, dy in p:
        if d == 1:
            dx, dy = -dy, dx
        if d == 2:
            dx, dy = -dx, -dy
        if d == 3:
            dx, dy = dy, -dx

        f[x + dx][y + dy] = pn

    return True


def isFull(f, n):
    for i in range(n):
        for j in range(n):
            if f[i][j] == EMPTY_CELL:
                return False

    return True


def main(polyomino, n, f, pn, result):
    if len(polyomino) == 0:
        return

    p = polyomino.pop()

    for i in range(n):
        for j in range(n):
            if f[i][j] != EMPTY_CELL:
                continue
            for d in range(4):
                if putPolyomino(f, n, p, pn, i, j, d) is None:
                    continue

                if isFull(f, n):
                    key = frozenset((itertools.chain.from_iterable(f)))
                    result[key] = result.get(key, 0) + 1
                    deletePolyomino(f, n, p, i, j, d)
                    continue

                main(polyomino, n, f, pn + 1, result)
                deletePolyomino(f, n, p, i, j, d)

    main(polyomino, n, f, pn + 1, result)
    polyomino.append(p)


n = 3
result = {}
f = [[EMPTY_CELL for _ in range(n)] for _ in range(n)]

polyomino = polyominoList.getPolyomino()
polyominoRoutate = polyominoList.getPolyominoRotate()

main(polyomino, n, f, 0, result)

answer = []
polyominoRoutate.reverse()
for k, v in result.items():
    count = functools.reduce(operator.floordiv, map(lambda y: 4 // polyominoRoutate[y], k), v)
    if count == 4:
        answer.append(k)

print(result)
print(answer)
