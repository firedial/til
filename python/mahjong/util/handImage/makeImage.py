from PIL import Image

HIGHT = 32
WIDTH = 24


def makeImage(number: str, hand: list[int], atama: int) -> None:
    sozuImage = []
    # 1 始まりとしてするためダミーデータを入れる
    sozuImage.append(Image.open("./image/sozu/p_ss1_1.gif"))

    for i in range(1, 10):
        sozuImage.append(Image.open("./image/sozu/p_ss" + str(i) + "_1.gif"))

    handLength = sum(hand) + atama
    handImage = Image.new("RGB", (WIDTH * handLength, HIGHT))

    count = 0
    if atama == 2:
        p1 = Image.open("./image/pinzu/p_ps1_1.gif")
        handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
        count += 1
        handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
        count += 1
        p1.close()
    elif atama == 5:
        p1 = Image.open("./image/pinzu/p_ps1_1.gif")
        p2 = Image.open("./image/pinzu/p_ps2_1.gif")
        p3 = Image.open("./image/pinzu/p_ps3_1.gif")
        handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
        count += 1
        handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
        count += 1
        handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
        count += 1
        handImage.paste(p2.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
        count += 1
        handImage.paste(p3.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
        count += 1
        p1.close()
        p2.close()
        p3.close()

    for i, h in enumerate(hand):
        for _ in range(h):
            handImage.paste(sozuImage[i + 1].resize((WIDTH, HIGHT)), (WIDTH * count, 0))
            count += 1

    # handImage.save("./image/result/" + number + ".gif")
    handImage.save("./" + number + ".gif")

    for i in range(0, 10):
        sozuImage[i].close()


def makeWaitImage(number: str, wait: list[int], atamaWait: int) -> None:
    sozuImage = []
    # 1 始まりとしてするためダミーデータを入れる
    sozuImage.append(Image.open("./image/sozu/p_ss1_1.gif"))

    for i in range(1, 10):
        sozuImage.append(Image.open("./image/sozu/p_ss" + str(i) + "_1.gif"))

    handLength = sum(wait) + atamaWait
    handImage = Image.new("RGB", (WIDTH * handLength, HIGHT))

    count = 0

    for i, h in enumerate(wait):
        for _ in range(h):
            handImage.paste(sozuImage[i + 1].resize((WIDTH, HIGHT)), (WIDTH * count, 0))
            count += 1

    for i in range(0, 10):
        sozuImage[i].close()

    if atamaWait == 1:
        p1 = Image.open("./image/pinzu/p_ps1_1.gif")
        handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
        count += 1
        p1.close()
    elif atamaWait == 2:
        p1 = Image.open("./image/pinzu/p_ps1_1.gif")
        p4 = Image.open("./image/pinzu/p_ps4_1.gif")
        handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
        count += 1
        handImage.paste(p4.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
        count += 1
        p1.close()
        p4.close()

    handImage.save("./image/result/" + number + ".gif")


def kokushiImage() -> None:
    handImage = Image.new("RGB", (WIDTH * 13, HIGHT))

    count = 0

    p1 = Image.open("./image/manzu/p_ms1_1.gif")
    handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
    count += 1
    p1.close
    p1 = Image.open("./image/manzu/p_ms9_1.gif")
    handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
    count += 1
    p1.close

    # p1 = Image.open("./image/pinzu/p_ps1_1.gif")
    # handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
    # count += 1
    # p1.close
    p1 = Image.open("./image/pinzu/p_ps9_1.gif")
    handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
    count += 1
    p1.close

    p1 = Image.open("./image/sozu/p_ss1_1.gif")
    handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
    count += 1
    p1.close

    p1 = Image.open("./image/sozu/p_ss9_1.gif")
    handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
    count += 1
    p1.close

    for i in range(1, 8):
        p1 = Image.open("./image/jihai/p_ji" + str(i) + "_1.gif")
        handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
        count += 1
        if i == 3:
            handImage.paste(p1.resize((WIDTH, HIGHT)), (WIDTH * count, 0))
            count += 1

        p1.close

    handImage.save("tmp.gif")


makeImage("tmp", [0, 1, 2, 1], 0)
