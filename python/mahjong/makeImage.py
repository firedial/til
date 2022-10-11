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

    handImage.save("./image/result/" + number + ".gif")

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


# makeImage("W000", [2], 2)
