import polyominoList


def makeFIle(n, ids, patternCount):
    polyominos = list(filter(lambda x: x["id"] > 0 and x["hasMirrored"] and not x["hasBlock"] and not x["hasConcave"], polyominoList.getPolyominos().values()))
    targetPolyominos = list(filter(lambda x: x["id"] in ids, polyominos))

    fp = open("./data/data_" + str(patternCount) + ".txt", mode="w")

    fp.write(str(n) + " " + str(n))
    fp.write("\n")
    for _ in range(n):
        for _ in range(n):
            fp.write("-")
        fp.write("\n")
    fp.write(str(len(targetPolyominos)))
    fp.write("\n")
    for polyomino in targetPolyominos:
        xmax = max(map(lambda x: x[0], polyomino["form"]))
        xmin = min(map(lambda x: x[0], polyomino["form"]))
        ymax = max(map(lambda x: x[1], polyomino["form"]))
        ymin = min(map(lambda x: x[1], polyomino["form"]))

        fp.write(str(xmax - xmin + 1) + " " + str(ymax - ymin + 1) + " " + str(polyomino["id"]))
        fp.write("\n")
        f = [[0 for _ in range(ymin, ymax + 1)] for _ in range(xmin, xmax + 1)]

        for i, j in polyomino["form"]:
            f[i - xmin][j - ymin] = 1
        for rows in f:
            for cell in rows:
                if cell == 1:
                    fp.write("#")
                else:
                    fp.write(".")
            fp.write("\n")

    fp.close()


patternCount = 0


def makePattern(n, polyominos, polyominoList):
    global patternCount

    s = sum(map(lambda x: x["count"], polyominoList))
    if n * n == s:
        patternCount += 1
        ids = list(map(lambda x: x["id"], polyominoList))
        makeFIle(n, ids, patternCount)

    if n * n < s or len(polyominos) == 0:
        return

    p = polyominos.pop()
    polyominoList.append(p)
    makePattern(n, polyominos, polyominoList)

    polyominoList.pop()
    makePattern(n, polyominos, polyominoList)
    polyominos.append(p)


allPolyominos = polyominoList.getPolyominos()
targetPolyominos = list(filter(lambda x: x["id"] > 0 and x["hasMirrored"] and not x["hasBlock"] and not x["hasConcave"], polyominoList.getPolyominos().values()))
ids = [31, 28, 27, 26, 24, 12, 7, 5, 2]
n = 7

makePattern(n, targetPolyominos, [])
