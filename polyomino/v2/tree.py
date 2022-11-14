import polyominoList
import copy

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

    return list(map(lambda x: set(x), hash))


def main(countField, polyominosPlaces):
    count = 0

    minIndex = countField.index(min(countField))

    # 当該セルに置けるポリオミノはないので抜ける
    if countField[minIndex] == 0:
        return 0

    # 最小値が埋まっているセルを表す数字であれば全部埋まっている
    if countField[minIndex] == FILL_CELL:
        return 1

    # この二重ループで、対象のセルのパターンを全部試す
    for id, polyominoPlaces in polyominosPlaces.items():
        for place in polyominoPlaces[minIndex]:

            # 除去処理
            popedPolyominosPlaces = copy.deepcopy(polyominosPlaces)
            nextCountField = countField.copy()
            popedPolyominosPlaces.pop(id)

            # ポリオミノを置く処理
            for cell in place:
                # 置いたことを表す
                nextCountField[cell] = FILL_CELL

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

            count += main(nextCountField, popedPolyominosPlaces)

    return count


n = 3
allPolyominos = polyominoList.getPolyominos()
polyominos = {3: allPolyominos[3], 9: allPolyominos[9]}
# polyominos = allPolyominos
countField = [0] * (n * n)
polyominosPlaces = {}

# 置くことができる場所を全て洗い出す
for polyomino in polyominos.values():
    polyominosPlaces[polyomino["id"]] = getPlaces(n, polyomino)

# 各セルに対して置ける個数を求める
for polyominoPlace in polyominosPlaces.values():
    for index, place in enumerate(polyominoPlace):
        countField[index] += len(place)


count = main(countField, polyominosPlaces)
print(count)
