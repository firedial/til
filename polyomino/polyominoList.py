poly = {
    1: {"id": 1, "hasMirrored": False, "rotate": 1, "count": 1, "form": [(0, 0)]},
    2: {"id": 2, "hasMirrored": False, "rotate": 2, "count": 2, "form": [(0, 0), (0, 1)]},
    3: {"id": 3, "hasMirrored": False, "rotate": 2, "count": 3, "form": [(0, 0), (0, 1), (0, 2)]},
    4: {"id": 4, "hasMirrored": False, "rotate": 4, "count": 3, "form": [(0, 0), (0, 1), (1, 0)]},
    5: {"id": 5, "hasMirrored": False, "rotate": 2, "count": 4, "form": [(0, 0), (0, 1), (0, 2), (0, 3)]},
    6: {"id": 6, "hasMirrored": False, "rotate": 1, "count": 4, "form": [(0, 0), (0, 1), (1, 0), (1, 1)]},
    7: {"id": 7, "hasMirrored": True, "rotate": 4, "count": 4, "form": [(0, 0), (0, 1), (1, 0), (2, 0)]},
    -7: {"id": -7, "hasMirrored": True, "rotate": 4, "count": 4, "form": [(0, 0), (0, 1), (-1, 0), (-2, 0)]},
    8: {"id": 8, "hasMirrored": True, "rotate": 2, "count": 4, "form": [(0, 0), (0, 1), (1, 1), (1, 2)]},
    -8: {"id": -8, "hasMirrored": True, "rotate": 2, "count": 4, "form": [(0, 0), (0, 1), (-1, 1), (-1, 2)]},
    9: {"id": 9, "hasMirrored": False, "rotate": 4, "count": 4, "form": [(0, 0), (0, 1), (1, 1), (0, 2)]},
    10: {"id": 10, "hasMirrored": False, "rotate": 2, "count": 5, "form": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]},
    11: {"id": 11, "hasMirrored": True, "rotate": 4, "count": 5, "form": [(0, 0), (-1, 0), (0, -1), (0, 1), (1, 1)]},
    -11: {"id": -11, "hasMirrored": True, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (0, -1), (0, 1), (-1, 1)]},
    12: {"id": 12, "hasMirrored": True, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3)]},
    -12: {"id": -12, "hasMirrored": True, "rotate": 4, "count": 5, "form": [(0, 0), (-1, 0), (-1, 1), (-1, 2), (-1, 3)]},
    13: {"id": 13, "hasMirrored": True, "rotate": 4, "count": 5, "form": [(0, 0), (0, 1), (0, 2), (-1, 1), (-1, 2)]},
    -13: {"id": -13, "hasMirrored": True, "rotate": 4, "count": 5, "form": [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)]},
    14: {"id": 14, "hasMirrored": True, "rotate": 4, "count": 5, "form": [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)]},
    -14: {"id": -14, "hasMirrored": True, "rotate": 4, "count": 5, "form": [(0, 0), (0, 1), (-1, 1), (-1, 2), (-1, 3)]},
    15: {"id": 15, "hasMirrored": False, "rotate": 4, "count": 5, "form": [(0, 0), (0, 1), (0, 2), (-1, 2), (1, 2)]},
    16: {"id": 16, "hasMirrored": False, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (-1, 0), (-1, 1)]},
    17: {"id": 17, "hasMirrored": False, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]},
    18: {"id": 18, "hasMirrored": False, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]},
    19: {"id": 19, "hasMirrored": False, "rotate": 1, "count": 5, "form": [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]},
    20: {"id": 20, "hasMirrored": True, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (1, -1), (1, -2)]},
    -20: {"id": -20, "hasMirrored": True, "rotate": 4, "count": 5, "form": [(0, 0), (-1, 0), (-1, 1), (-1, -1), (-1, -2)]},
    21: {"id": 21, "hasMirrored": True, "rotate": 2, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)]},
    -21: {"id": -21, "hasMirrored": True, "rotate": 2, "count": 5, "form": [(0, 0), (-1, 0), (-1, 1), (-1, 2), (-2, 2)]},
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
        print(v["id"], v["count"], v["rotate"])
        printPolyomino(v)
