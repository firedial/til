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


def printQr(fp, qr1, qr2):
    for i in range(SIZE):
        for j in range(SIZE):
            if qr1[i][j] == 0:
                fp.write("■")
            else:
                fp.write("□")

        fp.write("        ")
        for j in range(SIZE):
            if qr2[i][j] == 0:
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
    hasCorner = False
    for i in range(FRAME_SIZE):
        for j in range(FRAME_SIZE):
            if p[i][j] == n:
                polyomino[i][j] = n
                if i == 0 and j == 0:
                    hasCorner = True
                if i == FRAME_SIZE - 1 and j == 0:
                    hasCorner = True
                if i == 0 and j == FRAME_SIZE - 1:
                    hasCorner = True
            else:
                polyomino[i][j] = BLANK
    return hasCorner


def change(p1, p2, qr):
    numbers = set()
    for i in range(FRAME_SIZE):
        for j in range(FRAME_SIZE):
            numbers.add(p1[i][j])

    polyomino = [[BLANK for _ in range(FRAME_SIZE)] for _ in range(FRAME_SIZE)]
    afterQr = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    reflectionCount = 0
    cornerReflectionCount = 0
    for n in numbers:
        hasCorner = getPolyomino(polyomino, p1, n)
        isReflection = movePiece(polyomino, p2, qr, afterQr)
        if isReflection:
            reflectionCount += 1
            if hasCorner:
                cornerReflectionCount += 1

    return (afterQr, reflectionCount, cornerReflectionCount, len(numbers))


def getAfterQr(id: int, pattern: str, d: int, qr):
    # 敷き詰めパターンの読み込み
    directoryName = (id // 1000) * 1000
    tiles = []
    path = "./result/r" + str(directoryName) + "/result_" + str(id) + ".txt"
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

    if pattern == "A":
        before = rotate(FRAME_SIZE, tile1, d, False)
        after = tile2
        return change(before, after, qr)
    else:
        before = rotate(FRAME_SIZE, tile2, d, False)
        after = tile1
        return change(before, after, qr)


def hasSquare(qr):
    for (i, j) in itertools.product(range(SIZE - 2), range(SIZE - 2)):
        for (p, q) in itertools.product(range(3), range(3)):
            if qr[i + p][j + q] == 1:
                break
        else:
            return True

    return False


def hasL(qr):
    l1 = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1],
    ]
    l2 = [
        [0, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    l3 = [
        [1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    l4 = [
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 0],
    ]

    for x in [l1, l2, l3, l4]:
        for (i, j) in itertools.product(range(SIZE - 6), range(SIZE - 6)):
            for (p, q) in itertools.product(range(7), range(7)):
                if x[p][q] == 1:
                    continue
                if qr[i + p][j + q] == 1:
                    break
            else:
                return True

    return False


def save(fp, title, qr1, qr2):
    fp.write(title + "\n")
    printQr(fp, qr1, qr2)
    fp.write("\n")


# 対象となる QR コード
img = Image.open("test.png")
whiteImg = Image.open("white.png")
qr = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
whiteQr = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

# QR コードを符号化
for i in range(SIZE):
    for j in range(SIZE):
        color = img.getpixel((LEFT + j * PIXEL, UP + i * PIXEL))
        if color == 0:
            qr[i][j] = 0
        else:
            qr[i][j] = 1

        color = whiteImg.getpixel((LEFT + j * PIXEL, UP + i * PIXEL))
        if color[0] == 0:
            whiteQr[i][j] = 0
        else:
            whiteQr[i][j] = 1


ids0 = [
    27,
    54,
    55,
    63,
    90,
    96,
    97,
    106,
    107,
    111,
    116,
    118,
    124,
    131,
    148,
    187,
    200,
    206,
    208,
    229,
    247,
    248,
    251,
    258,
    271,
    276,
    314,
    329,
    336,
    347,
    348,
    380,
    382,
    385,
    388,
    402,
    404,
    428,
    444,
    451,
    482,
    546,
    592,
    663,
    679,
    703,
    711,
    725,
    744,
    753,
    764,
    772,
    776,
    791,
    804,
    821,
    827,
    842,
    847,
    852,
    875,
    883,
    884,
    886,
    896,
    917,
    924,
    926,
    943,
    948,
    962,
    972,
    982,
]

ids1000 = [
    1014,
    1022,
    1066,
    1067,
    1072,
    1079,
    1159,
    1160,
    1162,
    1166,
    1167,
    1168,
    1193,
    1203,
    1246,
    1263,
    1276,
    1284,
    1289,
    1291,
    1295,
    1298,
    1304,
    1308,
    1320,
    1334,
    1353,
    1355,
    1358,
    1372,
    1397,
    1404,
    1407,
    1414,
    1446,
    1483,
    1484,
    1501,
    1503,
    1514,
    1522,
    1527,
    1532,
    1561,
    1565,
    1581,
    1584,
    1587,
    1599,
    1624,
    1663,
    1722,
    1763,
    1802,
    1806,
    1843,
    1851,
]

ids2000 = [
    2007,
    2025,
    2029,
    2034,
    2049,
    2053,
    2060,
    2079,
    2080,
    2082,
    2087,
    2108,
    2118,
    2122,
    2148,
    2165,
    2171,
    2175,
    2177,
    2185,
    2190,
    2194,
    2199,
    2200,
    2202,
    2227,
    2243,
    2244,
    2245,
    2255,
    2258,
    2281,
    2289,
    2339,
    2342,
    2351,
    2385,
    2400,
    2475,
    2481,
    2501,
    2519,
    2534,
    2539,
    2547,
    2550,
    2562,
    2590,
    2591,
    2592,
    2596,
    2607,
    2610,
    2613,
    2617,
    2619,
    2621,
    2626,
    2630,
    2634,
    2665,
    2688,
    2706,
    2710,
    2717,
    2723,
    2748,
    2763,
    2815,
    2816,
    2818,
    2832,
    2835,
    2836,
    2854,
    2855,
    2870,
    2888,
    2891,
    2896,
    2903,
    2904,
    2912,
    2918,
    2930,
    2941,
    2947,
    2959,
    2960,
]

ids3000 = [
    3038,
    3043,
    3047,
    3084,
    3088,
    3092,
    3098,
    3134,
    3161,
    3315,
    3323,
    3333,
    3339,
    3340,
    3347,
    3369,
    3382,
    3391,
    3394,
    3412,
    3419,
    3427,
    3455,
    3463,
    3468,
    3474,
    3486,
    3501,
    3518,
    3547,
    3550,
    3557,
    3568,
    3574,
    3578,
    3579,
    3587,
    3664,
    3667,
    3676,
    3680,
    3710,
    3721,
    3725,
    3727,
    3737,
    3748,
    3754,
    3790,
    3792,
    3800,
    3802,
    3861,
    3874,
    3887,
    3898,
    3912,
    3927,
    3930,
    3939,
    3942,
    3950,
    3962,
    3966,
]

ids4000 = [
    4010,
    4015,
    4030,
    4083,
    4153,
    4163,
    4171,
    4184,
    4200,
    4256,
    4258,
    4260,
    4264,
    4276,
    4296,
    4298,
    4369,
    4381,
    4385,
    4391,
    4401,
    4426,
    4442,
    4444,
    4507,
    4522,
    4524,
    4536,
    4551,
    4594,
    4660,
    4662,
    4698,
    4714,
    4715,
    4736,
    4744,
    4785,
    4788,
    4804,
    4807,
    4822,
    4866,
    4872,
    4926,
    4938,
]

ids5000 = [
    5011,
    5047,
    5068,
]

count = 0
fp = open("./result.txt", mode="w", encoding="utf-8")
for id in ids0:
    for d in range(4):
        for p in ["A", "B"]:
            afterWhiteQr, r, cr, n = getAfterQr(id, p, d, whiteQr)

            # if hasSquare(afterWhiteQr):
            #     continue
            # if hasL(afterWhiteQr):
            #     continue
            # if cr == 0 or cr == 3:
            #     continue

            afterQr, r, cr, n = getAfterQr(id, p, d, qr)

            count += 1
            title = str(id) + p + str(d) + " n:" + str(n) + " r:" + str(r) + " cr:" + str(cr) + " square3:" + str(hasSquare(afterWhiteQr)) + " l7:" + str(hasL(afterWhiteQr))
            save(fp, title, afterWhiteQr, afterQr)
fp.close()

print(count)
