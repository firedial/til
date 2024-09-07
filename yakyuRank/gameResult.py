import csv
import datetime

# 2024/9/6 終了時点

central2024 = [
    [ # 広島
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 8, "l": 8, "d": 3, "r": 6},
        {"w": 11, "l": 10, "d": 1, "r": 3},
        {"w": 13, "l": 9, "d": 0, "r": 3},
        {"w": 7, "l": 12, "d": 1, "r": 5},
        {"w": 13, "l": 5, "d": 0, "r": 7},
        {"w": 10, "l": 8, "d": 0, "r": 0},
    ],
    [ # 巨人
        {"w": 8, "l": 8, "d": 3, "r": 6},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 11, "l": 11, "d": 1, "r": 2},
        {"w": 12, "l": 6, "d": 0, "r": 7},
        {"w": 12, "l": 9, "d": 1, "r": 3},
        {"w": 13, "l": 9, "d": 0, "r": 3},
        {"w": 8, "l": 9, "d": 1, "r": 0},
    ],
    [ # 阪神
        {"w": 10, "l": 11, "d": 1, "r": 3},
        {"w": 11, "l": 11, "d": 1, "r": 2},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 9, "l": 8, "d": 1, "r": 7},
        {"w": 14, "l": 7, "d": 3, "r": 1},
        {"w": 12, "l": 8, "d": 0, "r": 5},
        {"w": 7, "l": 11, "d": 0, "r": 0},
    ],
    [ # DeNA
        {"w": 9, "l": 13, "d": 0, "r": 3},
        {"w": 6, "l": 12, "d": 0, "r": 7},
        {"w": 8, "l": 9, "d": 1, "r": 7},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 12, "l": 7, "d": 1, "r": 5},
        {"w": 14, "l": 9, "d": 0, "r": 2},
        {"w": 11, "l": 7, "d": 0, "r": 0},
    ],
    [ # 中日
        {"w": 12, "l": 7, "d": 1, "r": 5},
        {"w": 9, "l": 12, "d": 1, "r": 3},
        {"w": 7, "l": 14, "d": 3, "r": 1},
        {"w": 7, "l": 12, "d": 1, "r": 5},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 9, "l": 9, "d": 2, "r": 5},
        {"w": 7, "l": 11, "d": 0, "r": 0},
    ],
    [ # ヤクルト
        {"w": 5, "l": 13, "d": 0, "r": 7},
        {"w": 9, "l": 13, "d": 0, "r": 3},
        {"w": 8, "l": 12, "d": 0, "r": 5},
        {"w": 9, "l": 14, "d": 0, "r": 2},
        {"w": 9, "l": 9, "d": 2, "r": 5},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 9, "l": 7, "d": 2, "r": 0},
    ],
]

# 2024/9/6 終了時点

pacific2024 = [
    [ # ソフトバンク
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 11, "l": 9, "d": 1, "r": 4},
        {"w": 15, "l": 8, "d": 1, "r": 1},
        {"w": 11, "l": 9, "d": 0, "r": 5},
        {"w": 10, "l": 6, "d": 1, "r": 8},
        {"w": 15, "l": 6, "d": 0, "r": 4},
        {"w": 12, "l": 6, "d": 0, "r": 0},
    ],
    [ # 日本ハム
        {"w": 9, "l": 11, "d": 1, "r": 4},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 17, "l": 6, "d": 1, "r": 1},
        {"w": 10, "l": 6, "d": 2, "r": 7},
        {"w": 10, "l": 10, "d": 1, "r": 4},
        {"w": 11, "l": 7, "d": 2, "r": 5},
        {"w": 7, "l": 10, "d": 1, "r": 0},
    ],
    [ # ロッテ
        {"w": 8, "l": 15, "d": 1, "r": 1},
        {"w": 6, "l": 17, "d": 1, "r": 1},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 10, "l": 7, "d": 1, "r": 7},
        {"w": 14, "l": 7, "d": 1, "r": 3},
        {"w": 16, "l": 1, "d": 0, "r": 8},
        {"w": 7, "l": 9, "d": 2, "r": 0},
    ],
    [ # 楽天
        {"w": 9, "l": 11, "d": 0, "r": 5},
        {"w": 6, "l": 10, "d": 2, "r": 7},
        {"w": 7, "l": 10, "d": 1, "r": 7},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 10, "l": 12, "d": 0, "r": 3},
        {"w": 13, "l": 10, "d": 0, "r": 2},
        {"w": 13, "l": 5, "d": 0, "r": 0},
    ],
    [ # オリックス
        {"w": 6, "l": 10, "d": 1, "r": 8},
        {"w": 10, "l": 10, "d": 1, "r": 4},
        {"w": 7, "l": 14, "d": 1, "r": 3},
        {"w": 12, "l": 10, "d": 0, "r": 3},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 12, "l": 11, "d": 0, "r": 2},
        {"w": 10, "l": 8, "d": 0, "r": 0},
    ],
    [ # 西武
        {"w": 6, "l": 15, "d": 0, "r": 4},
        {"w": 7, "l": 11, "d": 2, "r": 5},
        {"w": 1, "l": 16, "d": 0, "r": 8},
        {"w": 10, "l": 13, "d": 0, "r": 2},
        {"w": 11, "l": 12, "d": 0, "r": 2},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 4, "l": 14, "d": 0, "r": 0},
    ],
]


centralSetting = [
    {"name": "C", "color": "#BC0011", "index": 0},
    {"name": "G", "color": "#FF7820", "index": 1},
    {"name": "T", "color": "#FFE100", "index": 2},
    {"name": "DB", "color": "#0093C9", "index": 3},
    {"name": "D", "color": "#003595", "index": 4},
    {"name": "S", "color": "#96c800", "index": 5},
]

pacificSetting = [
    {"name": "H", "color": "#000000", "index": 0},
    {"name": "F", "color": "#01609A", "index": 1},
    {"name": "M", "color": "#CCCCCC", "index": 2},
    {"name": "E", "color": "#870010", "index": 3},
    {"name": "B", "color": "#AA9010", "index": 4},
    {"name": "L", "color": "#00215B", "index": 5},
]

def getData(initGameResult, resultFileName, setting, beforeTargetDate = None):
    mapping = dict([(team["name"], team["index"]) for team in setting])

    with open(resultFileName) as f:
        for row in csv.reader(f):
            if beforeTargetDate is not None:
                # beforeTageDate に設定された以前のものだけを集計する
                before = datetime.datetime.strptime(beforeTargetDate, "%Y-%m-%d")
                target = datetime.datetime.strptime(row[0], "%Y-%m-%d")
                if before < target:
                    continue

            t1 = mapping[row[1]]
            t2 = mapping[row[2]]

            if row[3] == 'w':
                initGameResult[t1][t2]['w'] += 1
                initGameResult[t1][t2]['r'] -= 1

                initGameResult[t2][t1]['l'] += 1
                initGameResult[t2][t1]['r'] -= 1
            elif row[3] == 'l':
                initGameResult[t1][t2]['l'] += 1
                initGameResult[t1][t2]['r'] -= 1

                initGameResult[t2][t1]['w'] += 1
                initGameResult[t2][t1]['r'] -= 1
            elif row[3] == 'd':
                initGameResult[t1][t2]['d'] += 1
                initGameResult[t1][t2]['r'] -= 1

                initGameResult[t2][t1]['d'] += 1
                initGameResult[t2][t1]['r'] -= 1

    return {"result": initGameResult, "setting": setting}

def getCentralData(beforeTargetDate = None):
    return getData(central2024, './result/centralResult.csv', centralSetting, beforeTargetDate)

def getPacificData(beforeTargetDate = None):
    return getData(pacific2024, './result/pacificResult.csv', pacificSetting, beforeTargetDate)
