import json

RATE = 1/7

originalData = '[{"index": 1, "max": 642, "now": 558, "min": 452, "win1": 652, "win2": 576, "win3": 574, "selfV": 608, "canSelfV": true, "lose1": 338, "lose2": 374, "lose3": 418, "win1Magic": null, "win2Magic": 17, "win3Magic": 17, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"index": 0, "max": 652, "now": 555, "min": 434, "win1": 642, "win2": 569, "win3": 569, "selfV": 598, "canSelfV": true, "lose1": 338, "lose2": 374, "lose3": 418, "win1Magic": 29, "win2Magic": 19, "win3Magic": 19, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"index": 2, "max": 598, "now": 513, "min": 423, "win1": 652, "win2": 598, "win3": 574, "selfV": 630, "canSelfV": false, "lose1": 338, "lose2": 374, "lose3": 418, "win1Magic": null, "win2Magic": 24, "win3Magic": 21, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"index": 3, "max": 595, "now": 500, "min": 404, "win1": 652, "win2": 598, "win3": 586, "selfV": 608, "canSelfV": false, "lose1": 338, "lose2": 374, "lose3": 467, "win1Magic": null, "win2Magic": null, "win3Magic": 26, "lose1Magic": null, "lose2Magic": null, "lose3Magic": -19}, {"index": 4, "max": 540, "now": 446, "min": 370, "win1": 652, "win2": 598, "win3": 586, "selfV": 620, "canSelfV": false, "lose1": 338, "lose2": 404, "lose3": 467, "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": null, "lose2Magic": -19, "lose3Magic": -10}, {"index": 5, "max": 539, "now": 423, "min": 338, "win1": 652, "win2": 598, "win3": 586, "selfV": 598, "canSelfV": false, "lose1": 370, "lose2": 407, "lose3": 453, "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": -24, "lose2Magic": -19, "lose3Magic": -12}]'
originalData = '[{"index": 0, "max": 707, "now": 637, "min": 514, "win1": 644, "win2": 605, "win3": 580, "selfV": 600, "canSelfV": true, "lose1": 255, "lose2": 378, "lose3": 421, "win1Magic": 19, "win2Magic": 13, "win3Magic": 10, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"index": 1, "max": 644, "now": 559, "min": 451, "win1": 707, "win2": 591, "win3": 580, "selfV": 664, "canSelfV": false, "lose1": 255, "lose2": 378, "lose3": 421, "win1Magic": null, "win2Magic": 19, "win3Magic": 18, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"index": 2, "max": 613, "now": 530, "min": 437, "win1": 707, "win2": 600, "win3": 586, "selfV": 685, "canSelfV": false, "lose1": 255, "lose2": 378, "lose3": 421, "win1Magic": null, "win2Magic": 23, "win3Magic": 21, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"index": 3, "max": 607, "now": 504, "min": 400, "win1": 707, "win2": 605, "win3": 600, "selfV": 671, "canSelfV": false, "lose1": 255, "lose2": 378, "lose3": 488, "win1Magic": null, "win2Magic": 29, "win3Magic": 28, "lose1Magic": null, "lose2Magic": null, "lose3Magic": -17}, {"index": 4, "max": 564, "now": 464, "min": 378, "win1": 707, "win2": 605, "win3": 600, "selfV": 650, "canSelfV": false, "lose1": 255, "lose2": 400, "lose3": 496, "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": null, "lose2Magic": -23, "lose3Magic": -10}, {"index": 5, "max": 439, "now": 313, "min": 255, "win1": 707, "win2": 605, "win3": 600, "selfV": 671, "canSelfV": false, "lose1": 378, "lose2": 421, "lose3": 464, "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": -9, "lose2Magic": -3, "lose3Magic": null}]'
data = json.loads(originalData)

for team in data:
    sortedTeam = dict(sorted(team.items(), key = lambda x: x[1] if x[1] is not None else 0, reverse = True))
    before = 1000
    record = ""

    for key, value in sortedTeam.items():
        if key not in ["max", "now", "min", "win1", "win2", "win3", "selfV", "lose1", "lose2", "lose3"]:
            continue

        record += "*" * int((before - value) * RATE)
        record += "┣" if key == "max" else ""
        record += "┫" if key == "min" else ""
        record += "○" if key == "now" else ""
        record += "①" + (str(team["win1Magic"]) if team["win1Magic"] is not None else "" ) if key == "win1" else ""
        record += "②" + (str(team["win2Magic"]) if team["win2Magic"] is not None else "" ) if key == "win2" else ""
        record += "③" + (str(team["win3Magic"]) if team["win3Magic"] is not None else "" ) if key == "win3" else ""
        record += "④" + (str(team["lose3Magic"]) if team["lose3Magic"] is not None else "" ) if key == "lose3" else ""
        record += "⑤" + (str(team["lose2Magic"]) if team["lose2Magic"] is not None else "" ) if key == "lose2" else ""
        record += "⑥" + (str(team["lose1Magic"]) if team["lose1Magic"] is not None else "" ) if key == "lose1" else ""
        record += "☆" if key == "selfV" else ""
        before = value

    record += "*" * int(before * RATE)
    print(record)




