import tkinter as tk
import json

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

pacificOriginalData = '[{"index": 0, "name": "H", "color": "#000000", "max": 707, "now": 640, "min": 521, "win1": 637, "win2": 598, "win3": 572, "selfV": 592, "canSelfV": true, "lose1": 262, "lose2": 385, "lose3": 421, "win1Magic": 17, "win2Magic": 11, "win3Magic": 8, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"index": 1, "name": "F", "color": "#01609A", "max": 637, "now": 554, "min": 451, "win1": 707, "win2": 591, "win3": 572, "selfV": 664, "canSelfV": false, "lose1": 262, "lose2": 385, "lose3": 421, "win1Magic": null, "win2Magic": 19, "win3Magic": 17, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"index": 2, "name": "M", "color": "#CCCCCC", "max": 605, "now": 526, "min": 437, "win1": 707, "win2": 592, "win3": 578, "selfV": 692, "canSelfV": false, "lose1": 262, "lose2": 385, "lose3": 421, "win1Magic": null, "win2Magic": 22, "win3Magic": 20, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"index": 3, "name": "E", "color": "#870010", "max": 600, "now": 500, "min": 400, "win1": 707, "win2": 598, "win3": 592, "selfV": 671, "canSelfV": false, "lose1": 262, "lose2": 385, "lose3": 488, "win1Magic": null, "win2Magic": 28, "win3Magic": 27, "lose1Magic": null, "lose2Magic": null, "lose3Magic": -16}, {"index": 4, "name": "B", "color": "#AA9010", "max": 564, "now": 469, "min": 385, "win1": 707, "win2": 598, "win3": 592, "selfV": 650, "canSelfV": false, "lose1": 262, "lose2": 400, "lose3": 496, "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": null, "lose2Magic": -23, "lose3Magic": -10}, {"index": 5, "name": "L", "color": "#00215B", "max": 439, "now": 318, "min": 262, "win1": 707, "win2": 598, "win3": 592, "selfV": 671, "canSelfV": false, "lose1": 385, "lose2": 421, "lose3": 464, "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": -8, "lose2Magic": -3, "lose3Magic": null}]'
centralOriginalData = '[{"index": 0, "name": "C", "color": "#BC0011", "max": 652, "now": 559, "min": 442, "win1": 635, "win2": 576, "win3": 574, "selfV": 591, "canSelfV": true, "lose1": 338, "lose2": 374, "lose3": 418, "win1Magic": 27, "win2Magic": 19, "win3Magic": 19, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"index": 1, "name": "G", "color": "#FF7820", "max": 635, "now": 553, "min": 452, "win1": 652, "win2": 576, "win3": 574, "selfV": 608, "canSelfV": true, "lose1": 338, "lose2": 374, "lose3": 418, "win1Magic": null, "win2Magic": 17, "win3Magic": 17, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"index": 2, "name": "T", "color": "#FFE100", "max": 598, "now": 517, "min": 430, "win1": 652, "win2": 591, "win3": 574, "selfV": 630, "canSelfV": false, "lose1": 338, "lose2": 374, "lose3": 418, "win1Magic": null, "win2Magic": 22, "win3Magic": 20, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"index": 3, "name": "DB", "color": "#0093C9", "max": 595, "now": 500, "min": 404, "win1": 652, "win2": 591, "win3": 589, "selfV": 608, "canSelfV": false, "lose1": 338, "lose2": 374, "lose3": 474, "win1Magic": null, "win2Magic": 27, "win3Magic": 27, "lose1Magic": null, "lose2Magic": null, "lose3Magic": -18}, {"index": 4, "name": "D", "color": "#003595", "max": 540, "now": 446, "min": 370, "win1": 652, "win2": 591, "win3": 589, "selfV": 613, "canSelfV": false, "lose1": 338, "lose2": 404, "lose3": 474, "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": null, "lose2Magic": -19, "lose3Magic": -9}, {"index": 5, "name": "S", "color": "#96c800", "max": 532, "now": 419, "min": 338, "win1": 652, "win2": 591, "win3": 589, "selfV": 594, "canSelfV": false, "lose1": 370, "lose2": 407, "lose3": 459, "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": -23, "lose2Magic": -18, "lose3Magic": -11}]'

originalData = pacificOriginalData
# originalData = centralOriginalData

data = json.loads(originalData)

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

