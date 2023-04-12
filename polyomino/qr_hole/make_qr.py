from PIL import Image, ImageDraw

UP = 40
LEFT = 40
SIZE = 21
PIXEL = 10

FRAME_SIZE = 7
CELL_SIZE = 3

BLANK = 0

assert SIZE == FRAME_SIZE * CELL_SIZE

# 対象となる QR コード
img = Image.open("hb1.png")
qr = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

# QR コードを符号化
for i in range(SIZE):
    for j in range(SIZE):
        color = img.getpixel((LEFT + j * PIXEL, UP + i * PIXEL))
        if color == 0:
            qr[i][j] = 0
        else:
            qr[i][j] = 1


D_FRAME = 1
D_HALF_DOT = 3

D_DOT = 2 * D_HALF_DOT
D_SIDE = 2

output = Image.new("RGB", (D_DOT * 21 + 2 * D_SIDE * D_DOT, D_DOT * 21 + 2 * D_SIDE * D_DOT), (255, 255, 255))
draw = ImageDraw.Draw(output)

for i in range(SIZE):
    for j in range(SIZE):
        if qr[i][j] == 0:
            draw.rectangle(
                (D_DOT * D_SIDE + D_DOT * i + D_FRAME, D_DOT * D_SIDE + D_DOT * j + D_FRAME, D_DOT * D_SIDE + D_DOT * (i + 1) - D_FRAME, D_DOT * D_SIDE + D_DOT * (j + 1) - D_FRAME), fill=(0, 0, 0)
            )

output.save("output.png")
