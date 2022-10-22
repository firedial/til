poly = [
    {"id": 1, "rotate": 1, "count": 1, "form": [(0, 0)]},
    {"id": 2, "rotate": 2, "count": 2, "form": [(0, 0), (0, 1)]},
    {"id": 3, "rotate": 2, "count": 3, "form": [(0, 0), (0, 1), (0, 2)]},
    {"id": 4, "rotate": 4, "count": 3, "form": [(0, 0), (0, 1), (1, 0)]},
    {"id": 5, "rotate": 2, "count": 4, "form": [(0, 0), (0, 1), (0, 2), (0, 3)]},
    {"id": 6, "rotate": 1, "count": 4, "form": [(0, 0), (0, 1), (1, 0), (1, 1)]},
    {"id": 7, "rotate": 4, "count": 4, "form": [(0, 0), (0, 1), (1, 0), (2, 0)]},
    {"id": 8, "rotate": 4, "count": 4, "form": [(0, 0), (0, 1), (1, 1), (1, 2)]},
    {"id": 9, "rotate": 4, "count": 4, "form": [(0, 0), (0, 1), (1, 1), (0, 2)]},
    {"id": 10, "rotate": 4, "count": 4, "form": [(0, 0), (0, 1), (1, 1), (1, 2)]},
    {"id": 11, "rotate": 4, "count": 4, "form": [(0, 0), (1, 0), (1, 1), (1, 2)]},
    {"id": 12, "rotate": 2, "count": 5, "form": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]},
    {"id": 13, "rotate": 4, "count": 5, "form": [(0, 0), (-1, 0), (0, -1), (0, 1), (1, 1)]},
    {"id": 14, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (0, -1), (0, 1), (-1, 1)]},
    {"id": 15, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3)]},
    {"id": 16, "rotate": 4, "count": 5, "form": [(0, 0), (-1, 0), (-1, 1), (-1, 2), (-1, 3)]},
    {"id": 17, "rotate": 4, "count": 5, "form": [(0, 0), (0, 1), (0, 2), (-1, 1), (-1, 2)]},
    {"id": 18, "rotate": 4, "count": 5, "form": [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)]},
    {"id": 19, "rotate": 4, "count": 5, "form": [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)]},
    {"id": 20, "rotate": 4, "count": 5, "form": [(0, 0), (0, 1), (-1, 1), (-1, 2), (-1, 3)]},
    {"id": 21, "rotate": 4, "count": 5, "form": [(0, 0), (0, 1), (0, 2), (-1, 2), (1, 2)]},
    {"id": 22, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (-1, 0), (-1, 1)]},
    {"id": 23, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]},
    {"id": 24, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]},
    {"id": 25, "rotate": 1, "count": 5, "form": [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]},
    {"id": 26, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (1, -1), (1, -2)]},
    {"id": 27, "rotate": 4, "count": 5, "form": [(0, 0), (-1, 0), (-1, 1), (-1, -1), (-1, -2)]},
    {"id": 28, "rotate": 4, "count": 5, "form": [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)]},
    {"id": 29, "rotate": 4, "count": 5, "form": [(0, 0), (-1, 0), (-1, 1), (-1, 2), (-2, 2)]},
]


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
    for p in poly:
        print("-" * 10)
        print(p["id"], p["count"], p["rotate"])
        printPolyomino(p)
