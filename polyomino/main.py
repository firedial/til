import copy
import itertools
import re


poly1 = [
    [(0, 0)],
]

poly2 = [
    [(0, 0), (0, 1)],
]

poly3 = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (0, 1), (1, 0)],
]

poly4 = [
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (0, 2)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
]

polyomino = poly1 + poly2 + poly3 + poly4


def deletePolyomino(f, n, p, x, y, d):
    for dx, dy in p:
        if d == 1:
            dx, dy = -dy, dx
        if d == 2:
            dx, dy = -dx, -dy
        if d == 3:
            dx, dy = dy, -dx

        f[x + dx][y + dy] = -1


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

        if f[x + dx][y + dy] != -1:
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
            if f[i][j] == -1:
                return False

    return True


def main(polyomino, n, f, pn, result):
    if len(polyomino) == 0:
        return

    p = polyomino.pop()

    for i in range(n):
        for j in range(n):
            if f[i][j] != -1:
                continue
            for d in range(4):
                if putPolyomino(f, n, p, pn, i, j, d) is None:
                    continue

                if isFull(f, n):
                    result.append(copy.deepcopy(f))
                    deletePolyomino(f, n, p, i, j, d)
                    continue

                main(polyomino, n, f, pn + 1, result)
                deletePolyomino(f, n, p, i, j, d)

    main(polyomino, n, f, pn + 1, result)
    polyomino.append(p)


n = 4
result = []
f = [[-1 for _ in range(n)] for _ in range(n)]

main(polyomino, n, f, 0, result)

print(result)
r = list(map(lambda x: set(itertools.chain.from_iterable(x)), result))
t = max(map(lambda x: len(x), r))
print(t)
