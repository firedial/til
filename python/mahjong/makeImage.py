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
        p2 = Image.open("./imgae/pinzu/p_ps2_1.gif")
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

    for h in hand:
        for _ in range(h):
            handImage.paste(sozuImage[h].resize((WIDTH, HIGHT)), (WIDTH * count, 0))
            count += 1

    handImage.save("./image/result/" + number + ".gif")

    for i in range(0, 10):
        sozuImage[i].close()


makeImage("W000", [2], 2)
