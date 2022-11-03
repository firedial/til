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

    return hash


def main(countField, polyominosPlaces):
    count = 0

    minIndex = countField.index(min(countField))

    # 当該セルに置けるポリオミノはないので抜ける
    if countField[minIndex] == 0:
        return 0

    # 最小値が埋まっているセルを表す数字であれば全部埋まっている
    if countField[minIndex] == FILL_CELL:
        return 1

    for id, polyominoPlaces in polyominosPlaces.items():
        for place in polyominoPlaces[minIndex]:
            # 除去処理
            popedPolyominosPlaces = copy.deepcopy(polyominosPlaces)
            nextCountField = copy.deepcopy(countField)
            popedPolyominosPlaces.pop(id)
            for cell in place:
                nextCountField[cell] = FILL_CELL

                for popedPolyominoPlaces in popedPolyominosPlaces.values():
                    popedPolyominoPlaces[cell] = []
                    nextCountField[cell] -= len(popedPolyominoPlaces[cell])

            count += main(nextCountField, popedPolyominosPlaces)

    return count


n = 5
allPolyominos = polyominoList.getPolyominos()
# polyominos = {3: allPolyominos[3], 9: allPolyominos[9]}
polyominos = allPolyominos
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
