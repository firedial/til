poly = {
    1: {"id": 1, "hasMirrored": False, "count": 3, "form": [(0, 0), (0, 1), (1, 0)]},
    2: {"id": 2, "hasMirrored": True, "count": 4, "form": [(0, 0), (0, 1), (1, 0), (2, 0)]},
    -2: {"id": -2, "hasMirrored": True, "count": 4, "form": [(0, 0), (0, 1), (-1, 0), (-2, 0)]},
    3: {"id": 3, "hasMirrored": False, "count": 4, "form": [(0, 0), (0, 1), (1, 1), (0, 2)]},
    4: {"id": 4, "hasMirrored": True, "count": 5, "form": [(0, 0), (-1, 0), (0, -1), (0, 1), (1, 1)]},
    -4: {"id": -4, "hasMirrored": True, "count": 5, "form": [(0, 0), (1, 0), (0, -1), (0, 1), (-1, 1)]},
    5: {"id": 5, "hasMirrored": True, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3)]},
    -5: {"id": -5, "hasMirrored": True, "count": 5, "form": [(0, 0), (-1, 0), (-1, 1), (-1, 2), (-1, 3)]},
    6: {"id": 6, "hasMirrored": True, "count": 5, "form": [(0, 0), (0, 1), (0, 2), (-1, 1), (-1, 2)]},
    -6: {"id": -6, "hasMirrored": True, "count": 5, "form": [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)]},
    7: {"id": 7, "hasMirrored": True, "count": 5, "form": [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)]},
    -7: {"id": -7, "hasMirrored": True, "count": 5, "form": [(0, 0), (0, 1), (-1, 1), (-1, 2), (-1, 3)]},
    8: {"id": 8, "hasMirrored": False, "count": 5, "form": [(0, 0), (0, 1), (0, 2), (-1, 2), (1, 2)]},
    9: {"id": 9, "hasMirrored": False, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (-1, 0), (-1, 1)]},
    10: {"id": 10, "hasMirrored": False, "count": 5, "form": [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]},
    11: {"id": 11, "hasMirrored": False, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]},
    12: {"id": 12, "hasMirrored": True, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (1, -1), (1, -2)]},
    -12: {"id": -12, "hasMirrored": True, "count": 5, "form": [(0, 0), (-1, 0), (-1, 1), (-1, -1), (-1, -2)]},
}


def printPolyomino(polyomino):
    n = polyomino["count"]
    f = [[0 for _ in range(-n, n + 1)] for _ in range(-n, n + 1)]

    for i, j in polyomino["form"]:
        f[n + i][n + j] = 1

    for rows in f:
        for cell in rows:
            if cell == 1:
                print("■", end="")
            else:
                print("□", end="")
        print()


def getPolyominos():
    return poly


if __name__ == "__main__":
    for k, v in poly.items():
        print("-" * 10)
        print(v["id"], v["count"])
        printPolyomino(v)
