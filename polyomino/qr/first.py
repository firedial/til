from PIL import Image
import itertools


UP = 40
LEFT = 40
SIZE = 21
PIXEL = 10

FRAME_SIZE = 7
CELL_SIZE = 3

BLANK = 0

assert SIZE == FRAME_SIZE * CELL_SIZE


def rotate(n, p, d, r):
    rp = [[0 for _ in range(n)] for _ in range(n)]
    center = n // 2

    for i in range(n):
        for j in range(n):
            dx = i - center
            dy = j - center

            if d == 1:
                dx, dy = -dy, dx
            if d == 2:
                dx, dy = -dx, -dy
            if d == 3:
                dx, dy = dy, -dx

            if r:
                dx, dy = dy, dx

            rp[i][j] = p[dx + center][dy + center]

    return rp


def isSame(n, p, q):
    for i in range(n):
        for j in range(n):
            if p[i][j] != q[i][j]:
                return False

    return True


def printQr(fp, qr):
    for i in range(SIZE):
        for j in range(SIZE):
            if qr[i][j] == 0:
                fp.write("■")
            else:
                fp.write("□")
        fp.write("\n")


def printTile(t):
    for i in range(FRAME_SIZE):
        for j in range(FRAME_SIZE):
            print(str(t[i][j]).zfill(2) + " ", end="")
        print()


def putPolyomino(polyomino, p, qr, afterQr, x, y, d, reflection):
    testPolyomino = rotate(FRAME_SIZE, polyomino, d, reflection)

    # 置けるかどうかをチェックする
    count = 0
    for i in range(FRAME_SIZE):
        for j in range(FRAME_SIZE):
            if polyomino[i][j] != BLANK:
                count += 1

            dx = i + x
            dy = j + y
            if not (0 <= dx < FRAME_SIZE):
                continue
            if not (0 <= dy < FRAME_SIZE):
                continue

            if testPolyomino[i][j] == BLANK:
                continue

            if testPolyomino[i][j] != p[dx][dy]:
                return False

            count -= 1

    if count != 0:
        return False

    movedQr = rotate(SIZE, qr, d, reflection)

    # 実際におく
    for i in range(FRAME_SIZE):
        for j in range(FRAME_SIZE):
            dx = i + x
            dy = j + y
            if not (0 <= dx < FRAME_SIZE):
                continue
            if not (0 <= dy < FRAME_SIZE):
                continue

            if testPolyomino[i][j] == BLANK:
                continue

            for s in range(3):
                for t in range(3):
                    afterQr[3 * dx + s][3 * dy + t] = movedQr[3 * i + s][3 * j + t]

    return True


def movePiece(polyomino, p2, qr, afterQr):
    for i in range(-1 * FRAME_SIZE + 1, FRAME_SIZE):
        for j in range(-1 * FRAME_SIZE + 1, FRAME_SIZE):
            for d in range(4):
                for reflection in [True, False]:
                    if putPolyomino(polyomino, p2, qr, afterQr, i, j, d, reflection):
                        if reflection:
                            return 1
                        else:
                            return 0


def getPolyomino(polyomino, p, n):
    for i in range(FRAME_SIZE):
        for j in range(FRAME_SIZE):
            if p[i][j] == n:
                polyomino[i][j] = n
            else:
                polyomino[i][j] = BLANK


def change(p1, p2, qr):
    numbers = set()
    for i in range(FRAME_SIZE):
        for j in range(FRAME_SIZE):
            numbers.add(p1[i][j])

    polyomino = [[BLANK for _ in range(FRAME_SIZE)] for _ in range(FRAME_SIZE)]
    afterQr = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    reflectionCount = 0
    for n in numbers:
        getPolyomino(polyomino, p1, n)
        reflectionCount += movePiece(polyomino, p2, qr, afterQr)

    return (afterQr, reflectionCount)


def displayChange(id: int):
    # 敷き詰めパターンの読み込み
    tiles = []
    path = "./result_" + str(id) + ".txt"
    with open(path, mode="r") as fp:
        lines = fp.readlines()

        count = 0
        tile = []
        for line in lines:
            count += 1
            if count == 1:
                continue

            tile.append(list(map(lambda x: int(x), line[1:].strip().split("|"))))

            if count == FRAME_SIZE + 1:
                tiles.append(tile)
                count = 0
                tile = []

            if len(tiles) == 16:
                break

    tile1 = tiles[-1]
    tile2 = tiles[-1]

    for i in range(15):
        for (d, r) in itertools.product(range(4), [True, False]):
            if isSame(FRAME_SIZE, tile1, rotate(FRAME_SIZE, tiles[i], d, r)):
                break
        else:
            tile2 = tiles[i]
            break

    fp = open("./result.txt", mode="w", encoding="utf-8")

    for d in range(4):
        before = rotate(FRAME_SIZE, tile1, d, False)
        after = tile2
        (afterQr, reflectionCount) = change(before, after, qr)
        fp.write(str(id) + " " + "A" + str(d) + " " + "r:" + str(reflectionCount))
        fp.write("\n")
        printQr(fp, afterQr)
        fp.write("\n")

        before = rotate(FRAME_SIZE, tile2, d, False)
        after = tile1
        (afterQr, reflectionCount) = change(before, after, qr)
        fp.write(str(id) + " " + "B" + str(d) + " " + "r:" + str(reflectionCount))
        fp.write("\n")
        printQr(fp, afterQr)
        fp.write("\n")

    fp.close()


# 対象となる QR コード
img = Image.open("test.png")
qr = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

# QR コードを符号化
for i in range(SIZE):
    for j in range(SIZE):
        color = img.getpixel((LEFT + j * PIXEL, UP + i * PIXEL))
        if color[0] == 0:
            qr[i][j] = 0
        else:
            qr[i][j] = 1

displayChange(63)
