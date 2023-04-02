from PIL import Image

UP = 40
LEFT = 40
SIZE = 21
PIXEL = 10

FRAME_SIZE = 7
CELL_SIZE = 3

BLANK = 0

assert SIZE == FRAME_SIZE * CELL_SIZE

# 対象となる QR コード
img = Image.open("test.png")
qr = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

# QR コードを符号化
for i in range(SIZE):
    for j in range(SIZE):
        color = img.getpixel((LEFT + j * PIXEL, UP + i * PIXEL))
        if color == 0:
            qr[i][j] = 0
            print("■", end="")
        else:
            qr[i][j] = 1
            print("□", end="")

    print()
