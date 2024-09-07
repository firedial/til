import tkinter as tk
import json
import datetime
import sys


def getDisplayData(league: str, targetDate):
    with open("data.txt") as f:
        return sorted(
            filter(
                lambda data: data['league'] == league and datetime.datetime.strptime(data['date'], "%Y-%m-%d") <= targetDate,
                map(lambda rawData: json.loads(rawData), f.readlines()),
            ),
            key = lambda x: x['date'],
            reverse = True,
        )[0]


LEFT = 100
TOP = 100
DIFF = 150
WIDTH_RATE = 1.6


root = tk.Tk()
root.geometry("1800x1200")

# Canvasの作成
canvas = tk.Canvas(root, bg = "white")
# Canvasを配置
canvas.pack(fill = tk.BOTH, expand = True)

date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d")
centralOriginalData = getDisplayData('central', date)
pacificOriginalData = getDisplayData('pacific', date)

if sys.argv[2] == 'central':
    data = centralOriginalData['displayData']
elif sys.argv[2] == 'pacific':
    data = pacificOriginalData['displayData']
else:
    raise Exception('league is wrong')

for i, team in enumerate(data):
    left = LEFT
    top = TOP + i * DIFF
    color = team["color"]

    # ベースとなる線
    canvas.create_line(left, top, left + 1000 * WIDTH_RATE, top, fill = color, width = 3)
    canvas.create_text(left - 10, top, text = team["name"], font=("", 12), fill = color)

    # 最大値
    canvas.create_line(left + (1000 - team["max"]) * WIDTH_RATE, top - 10, left + (1000 - team["max"]) * WIDTH_RATE, top + 10, fill = color, width = 3)
    canvas.create_text(left + (1000 - team["max"]) * WIDTH_RATE, top - 20, text = team["max"], font=("", 12), fill = color)

    # 最小値
    canvas.create_line(left + (1000 - team["min"]) * WIDTH_RATE, top - 10, left + (1000 - team["min"]) * WIDTH_RATE, top + 10, fill = color, width = 3)
    canvas.create_text(left + (1000 - team["min"]) * WIDTH_RATE, top - 20, text = team["min"], font=("", 12), fill = color)

    # 現在値
    canvas.create_oval(left + (1000 - team["now"]) * WIDTH_RATE - 5, top - 5, left + (1000 - team["now"]) * WIDTH_RATE + 5, top + 5, fill = color, outline = color)
    canvas.create_text(left + (1000 - team["now"]) * WIDTH_RATE, top - 20, text = team["now"], font=("", 12), fill = color)

    # 自力優勝
    selfVString = "★" if team["canSelfV"] else "☆"
    canvas.create_text(left + (1000 - team["selfV"]) * WIDTH_RATE, top - 2, text = selfVString, font=("", 18), fill = color)

    # 上位ベースライン
    winBaseLine = 40

    # 上位
    canvas.create_line(left, top + winBaseLine, left + (1000 - team["min"]) * WIDTH_RATE, top + winBaseLine, fill = color, width = 1)
    canvas.create_line(left + (1000 - team["min"]) * WIDTH_RATE, top, left + (1000 - team["min"]) * WIDTH_RATE, top + winBaseLine, fill = color, width = 1)

    # 上位Magic
    if team["win1"] < team["min"]:
        canvas.create_text(left + (1000 - team["win1"]) * WIDTH_RATE, top, text = "①", font=("", 18), fill = color)
        canvas.create_text(left + (1000 - team["win1"]) * WIDTH_RATE, top - 20, text = team["lose1"], font=("", 12), fill = color)
    else:
        canvas.create_text(left + (1000 - team["win1"]) * WIDTH_RATE, top + winBaseLine, text = "①", font=("", 18), fill = color)
        canvas.create_text(left + (1000 - team["win1"]) * WIDTH_RATE, top + winBaseLine - 17, text = team["win1"], font=("", 12), fill = color)
        canvas.create_text(left + (1000 - team["win1"]) * WIDTH_RATE, top + winBaseLine + 17, text = team["win1Magic"], font=("", 12), fill = color)

    if team["win2"] < team["min"]:
        canvas.create_text(left + (1000 - team["win2"]) * WIDTH_RATE, top, text = "②", font=("", 18), fill = color)
        canvas.create_text(left + (1000 - team["win2"]) * WIDTH_RATE, top - 20, text = team["lose2"], font=("", 12), fill = color)
    else:
        canvas.create_text(left + (1000 - team["win2"]) * WIDTH_RATE, top + winBaseLine, text = "②", font=("", 18), fill = color)
        canvas.create_text(left + (1000 - team["win2"]) * WIDTH_RATE, top + winBaseLine - 17, text = team["win2"], font=("", 12), fill = color)
        canvas.create_text(left + (1000 - team["win2"]) * WIDTH_RATE, top + winBaseLine + 17, text = team["win2Magic"], font=("", 12), fill = color)

    if team["win3"] < team["min"]:
        canvas.create_text(left + (1000 - team["win3"]) * WIDTH_RATE, top, text = "③", font=("", 18), fill = color)
        canvas.create_text(left + (1000 - team["win3"]) * WIDTH_RATE, top - 20, text = team["lose3"], font=("", 12), fill = color)
    else:
        canvas.create_text(left + (1000 - team["win3"]) * WIDTH_RATE, top + winBaseLine, text = "③", font=("", 18), fill = color)
        canvas.create_text(left + (1000 - team["win3"]) * WIDTH_RATE, top + winBaseLine - 17, text = team["win3"], font=("", 12), fill = color)
        canvas.create_text(left + (1000 - team["win3"]) * WIDTH_RATE, top + winBaseLine + 17, text = team["win3Magic"], font=("", 12), fill = color)

    # 下位ベースライン
    loseBaseLine = 70

    # 下位
    canvas.create_line(left + (1000 - team["max"]) * WIDTH_RATE, top + loseBaseLine, left + 1000 * WIDTH_RATE, top + loseBaseLine, fill = color, width = 1)
    canvas.create_line(left + (1000 - team["max"]) * WIDTH_RATE, top, left + (1000 - team["max"]) * WIDTH_RATE, top + loseBaseLine, fill = color, width = 1)

    # 下位Magic
    if team["lose1"] > team["max"]:
        canvas.create_text(left + (1000 - team["lose1"]) * WIDTH_RATE, top, text = "⑥", font=("", 18), fill = color)
        canvas.create_text(left + (1000 - team["lose1"]) * WIDTH_RATE, top - 20, text = team["lose1"], font=("", 12), fill = color)
    else:
        canvas.create_text(left + (1000 - team["lose1"]) * WIDTH_RATE, top + loseBaseLine, text = "⑥", font=("", 18), fill = color)
        canvas.create_text(left + (1000 - team["lose1"]) * WIDTH_RATE, top + loseBaseLine - 17, text = team["lose1"], font=("", 12), fill = color)
        canvas.create_text(left + (1000 - team["lose1"]) * WIDTH_RATE, top + loseBaseLine + 17, text = team["lose1Magic"], font=("", 12), fill = color)

    if team["lose2"] > team["max"]:
        canvas.create_text(left + (1000 - team["lose2"]) * WIDTH_RATE, top, text = "⑤", font=("", 18), fill = color)
        canvas.create_text(left + (1000 - team["lose2"]) * WIDTH_RATE, top - 20, text = team["lose2"], font=("", 12), fill = color)
    else:
        canvas.create_text(left + (1000 - team["lose2"]) * WIDTH_RATE, top + loseBaseLine, text = "⑤", font=("", 18), fill = color)
        canvas.create_text(left + (1000 - team["lose2"]) * WIDTH_RATE, top + loseBaseLine - 17, text = team["lose2"], font=("", 12), fill = color)
        canvas.create_text(left + (1000 - team["lose2"]) * WIDTH_RATE, top + loseBaseLine + 17, text = team["lose2Magic"], font=("", 12), fill = color)

    if team["lose3"] > team["max"]:
        canvas.create_text(left + (1000 - team["lose3"]) * WIDTH_RATE, top, text = "④", font=("", 18), fill = color)
        canvas.create_text(left + (1000 - team["lose3"]) * WIDTH_RATE, top - 20, text = team["lose3"], font=("", 12), fill = color)
    else:
        canvas.create_text(left + (1000 - team["lose3"]) * WIDTH_RATE, top + loseBaseLine, text = "④", font=("", 18), fill = color)
        canvas.create_text(left + (1000 - team["lose3"]) * WIDTH_RATE, top + loseBaseLine - 17, text = team["lose3"], font=("", 12), fill = color)
        canvas.create_text(left + (1000 - team["lose3"]) * WIDTH_RATE, top + loseBaseLine + 17, text = team["lose3Magic"], font=("", 12), fill = color)


root.mainloop()

