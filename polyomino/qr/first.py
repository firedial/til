from PIL import Image

img = Image.open("test.png")

UP = 40
LEFT = 40
SIZE = 21
PIXEL = 10

FRAME_SIZE = 7
CELL_SIZE = 3

BLANK = 0

assert SIZE == FRAME_SIZE * CELL_SIZE


qr = [[0 for _ in range(SIZE)] for _ in range(SIZE)]


def printQr(qr):
    for i in range(SIZE):
        for j in range(SIZE):
            if qr[i][j] == 0:
                print("■", end="")
            else:
                print("□", end="")
        print()


def putPolyomino(polyomino, p, qr, afterQr, x, y, d, reflection):

    testPolyomino = [[BLANK for _ in range(FRAME_SIZE)] for _ in range(FRAME_SIZE)]
    center = FRAME_SIZE // 2

    for i in range(FRAME_SIZE):
        for j in range(FRAME_SIZE):
            dx = i - center
            dy = j - center

            if d == 1:
                dx, dy = -dy, dx
            if d == 2:
                dx, dy = -dx, -dy
            if d == 3:
                dx, dy = dy, -dx

            if reflection:
                dx, dy = dy, dx

            testPolyomino[i][j] = polyomino[dx + center][dy + center]

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

    movedQr = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    for i in range(SIZE):
        for j in range(SIZE):
            dx = i - 10
            dy = j - 10

            if d == 1:
                dx, dy = -dy, dx
            if d == 2:
                dx, dy = -dx, -dy
            if d == 3:
                dx, dy = dy, -dx

            if reflection:
                dx, dy = dy, dx

            movedQr[i][j] = qr[dx + 10][dy + 10]

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
                        return


def getPolyomino(polyomino, p, n):
    for i in range(FRAME_SIZE):
        for j in range(FRAME_SIZE):
            if p[i][j] == n:
                polyomino[i][j] = n
            else:
                polyomino[i][j] = BLANK


for i in range(SIZE):
    for j in range(SIZE):
        color = img.getpixel((LEFT + j * PIXEL, UP + i * PIXEL))
        if color == 0:
            qr[i][j] = 0
        else:
            qr[i][j] = 1


def rotate(p, d):
    testPolyomino = [[BLANK for _ in range(FRAME_SIZE)] for _ in range(FRAME_SIZE)]
    center = FRAME_SIZE // 2

    for i in range(FRAME_SIZE):
        for j in range(FRAME_SIZE):
            dx = i - center
            dy = j - center

            if d == 1:
                dx, dy = -dy, dx
            if d == 2:
                dx, dy = -dx, -dy
            if d == 3:
                dx, dy = dy, -dx

            testPolyomino[i][j] = p[dx + center][dy + center]

    return testPolyomino


p2 = [
    [2, 24, 12, 12, 12, 12, 14],
    [2, 24, 24, 24, 12, 14, 14],
    [2, 2, 24, 27, 27, 27, 14],
    [5, 28, 24, 27, 31, 31, 14],
    [5, 28, 27, 27, 4, 31, 14],
    [5, 28, 28, 4, 4, 31, 31],
    [5, 5, 28, 28, 4, 4, 31],
]

p1 = [
    [14, 5, 5, 5, 5, 31, 31],
    [14, 5, 4, 31, 31, 31, 27],
    [14, 4, 4, 31, 27, 27, 27],
    [14, 14, 4, 4, 27, 2, 2],
    [14, 28, 28, 28, 27, 24, 2],
    [28, 28, 12, 24, 24, 24, 2],
    [28, 12, 12, 12, 12, 24, 24],
]


def change(p1, p2, qr):
    numbers = set()
    for i in range(FRAME_SIZE):
        for j in range(FRAME_SIZE):
            numbers.add(p1[i][j])

    polyomino = [[BLANK for _ in range(FRAME_SIZE)] for _ in range(FRAME_SIZE)]
    afterQr = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    for n in numbers:
        getPolyomino(polyomino, p1, n)
        movePiece(polyomino, p2, qr, afterQr)

    return afterQr


before = rotate(p1, 1)
after = p2

afterQr = change(before, after, qr)
printQr(afterQr)

print()

after2Qr = change(after, before, afterQr)
printQr(after2Qr)
