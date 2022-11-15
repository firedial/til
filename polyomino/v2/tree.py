import polyominoList
import copy
import datetime
import math

FILL_CELL = 999999


def getPlaces(n, polyomino):
    hash = [[] for _ in range(n * n)]

    for i in range(n):
        for j in range(n):
            for d in range(4):
                place = []
                for dx, dy in polyomino["form"]:
                    if d == 1:
                        dx, dy = -dy, dx
                    elif d == 2:
                        dx, dy = -dx, -dy
                    elif d == 3:
                        dx, dy = dy, -dx

                    if not (0 <= (i + dx) < n):
                        break
                    if not (0 <= (j + dy) < n):
                        break

                    place.append((i + dx) * n + (j + dy))
                else:
                    for cell in place:
                        hash[cell].append(frozenset(place))

                mirroredPolyominoForm = list(map(lambda x: (x[0], -1 * x[1]), polyomino["form"]))
                place = []
                for dx, dy in mirroredPolyominoForm:
                    if d == 1:
                        dx, dy = -dy, dx
                    elif d == 2:
                        dx, dy = -dx, -dy
                    elif d == 3:
                        dx, dy = dy, -dx

                    if not (0 <= (i + dx) < n):
                        break
                    if not (0 <= (j + dy) < n):
                        break

                    place.append((i + dx) * n + (j + dy))
                else:
                    for cell in place:
                        hash[cell].append(frozenset(place))

    return list(map(lambda x: set(x), hash))


def printAns(ans):
    n = math.isqrt(len(ans))
    for index, id in enumerate(ans):
        if index % n == 0:
            print()
        print("{:3d}".format(id), end="")

    print()


def main(countField, polyominosPlaces, ans):
    count = 0

    minIndex = countField.index(min(countField))

    # 当該セルに置けるポリオミノはないので抜ける
    if countField[minIndex] == 0:
        return 0

    # 最小値が埋まっているセルを表す数字であれば全部埋まっている
    if countField[minIndex] == FILL_CELL:
        # printAns(ans)
        return 1

    # この二重ループで、対象のセルのパターンを全部試す
    for id, polyominoPlaces in polyominosPlaces.items():
        for place in polyominoPlaces[minIndex]:

            # 除去処理
            popedPolyominosPlaces = copy.deepcopy(polyominosPlaces)
            nextCountField = countField.copy()
            popedPolyominosPlaces.pop(id)
            nextAns = ans.copy()

            # ポリオミノを置く処理
            for cell in place:
                # 置いたことを表す
                nextCountField[cell] = FILL_CELL
                nextAns[cell] = id

                # 各ポリオミノと各セルに対して、除去する
                for removeId, removePolyominoPlaces in polyominosPlaces.items():
                    # すでにポップされている
                    if removeId == id:
                        continue

                    for removePolyominoPlace in removePolyominoPlaces[cell]:
                        for removeCell in removePolyominoPlace:
                            popedPolyominosPlaces[removeId][removeCell].discard(removePolyominoPlace)

            # 各セルに対して置ける個数を求める
            for popedPolyominoPlace in popedPolyominosPlaces.values():
                for index, place in enumerate(popedPolyominoPlace):
                    countField[index] += len(place)

            count += main(nextCountField, popedPolyominosPlaces, nextAns)

    return count


patternCount = 0


def makePattern(fp, allPolyominos, n, polyominos, polyominoList):
    global patternCount
    s = sum(map(lambda x: x["count"], polyominoList))
    if n * n == s:
        testPolyominoIdsList = [list(map(lambda x: x["id"], polyominoList))]

        for ids in testPolyominoIdsList:
            patternCount += 1
            if patternCount < 0:
                continue

            print(datetime.datetime.now(), patternCount)
            fp.write("--- " + str(patternCount) + " ---")
            fp.write("\n")
            fp.write(", ".join(map(lambda x: str(x), ids)))
            fp.write("\n")

            testPolyominoSet = dict(map(lambda x: (x, allPolyominos[x]), ids))

            # 置くことができる場所を全て洗い出す
            polyominosPlaces = {}
            for testPolyomino in testPolyominoSet.values():
                polyominosPlaces[testPolyomino["id"]] = getPlaces(n, testPolyomino)

            # 各セルに対して置ける個数を求める
            field = [0] * s
            for polyominoPlace in polyominosPlaces.values():
                for index, place in enumerate(polyominoPlace):
                    field[index] += len(place)

            ans = [0] * s
            count = main(field, polyominosPlaces, ans)
            print(count)
            fp.write("count: " + str(count))
            fp.write("\n")
            fp.write("pattern[" + str(count // 4) + "]")
            fp.write("\n")
            # if count == 8:
            #     fp.write("[ans] ")
            #     fp.write("\n")
            # uniqueCount = functools.reduce(operator.floordiv, map(lambda x: 4 // x["rotate"], testPolyominoSet), count)
            # result[frozenset(map(lambda x: x["id"], testPolyominoSet))] = uniqueCount // 4

        return

    if n * n < s or len(polyominos) == 0:
        return

    p = polyominos.pop()
    polyominoList.append(p)
    makePattern(fp, allPolyominos, n, polyominos, polyominoList)

    polyominoList.pop()
    makePattern(fp, allPolyominos, n, polyominos, polyominoList)
    polyominos.append(p)


n = 3
allPolyominos = polyominoList.getPolyominos()
targetPolyominos = list(filter(lambda x: x["id"] > 0 and x["hasMirrored"] and not x["hasBlock"] and not x["hasConcave"], polyominoList.getPolyominos().values()))
targetPolyominoIds = [14, 12, 7, 5, 2]
# targetPolyominos = list(filter(lambda x: x["id"] in targetPolyominoIds, targetPolyominos))

fp = open("result.txt", mode="w")
makePattern(fp, allPolyominos, n, targetPolyominos, [])
fp.close()
