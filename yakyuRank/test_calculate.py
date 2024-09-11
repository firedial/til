import unittest
import calculate
import json


central2024 = [
    [ # 広島
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 8, "l": 8, "d": 3, "r": 6},
        {"w": 11, "l": 10, "d": 1, "r": 3},
        {"w": 13, "l": 6, "d": 0, "r": 6},
        {"w": 7, "l": 11, "d": 1, "r": 6},
        {"w": 13, "l": 5, "d": 0, "r": 7},
        {"w": 10, "l": 8, "d": 0, "r": 0},
    ],
    [ # 巨人
        {"w": 8, "l": 8, "d": 3, "r": 6},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 11, "l": 11, "d": 1, "r": 2},
        {"w": 12, "l": 6, "d": 0, "r": 7},
        {"w": 12, "l": 9, "d": 1, "r": 3},
        {"w": 12, "l": 7, "d": 0, "r": 6},
        {"w": 8, "l": 9, "d": 1, "r": 0},
    ],
    [ # 阪神
        {"w": 10, "l": 11, "d": 1, "r": 3},
        {"w": 11, "l": 11, "d": 1, "r": 2},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 9, "l": 8, "d": 1, "r": 7},
        {"w": 11, "l": 7, "d": 3, "r": 4},
        {"w": 11, "l": 8, "d": 0, "r": 6},
        {"w": 7, "l": 11, "d": 0, "r": 0},
    ],
    [ # DeNA
        {"w": 6, "l": 13, "d": 0, "r": 6},
        {"w": 6, "l": 12, "d": 0, "r": 7},
        {"w": 8, "l": 9, "d": 1, "r": 7},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 12, "l": 7, "d": 1, "r": 5},
        {"w": 14, "l": 9, "d": 0, "r": 2},
        {"w": 11, "l": 7, "d": 0, "r": 0},
    ],
    [ # 中日
        {"w": 11, "l": 7, "d": 1, "r": 6},
        {"w": 9, "l": 12, "d": 1, "r": 3},
        {"w": 7, "l": 11, "d": 3, "r": 4},
        {"w": 7, "l": 12, "d": 1, "r": 5},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 9, "l": 9, "d": 2, "r": 5},
        {"w": 7, "l": 11, "d": 0, "r": 0},
    ],
    [ # ヤクルト
        {"w": 5, "l": 13, "d": 0, "r": 7},
        {"w": 7, "l": 12, "d": 0, "r": 6},
        {"w": 8, "l": 11, "d": 0, "r": 6},
        {"w": 9, "l": 14, "d": 0, "r": 2},
        {"w": 9, "l": 9, "d": 2, "r": 5},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 9, "l": 7, "d": 2, "r": 0},
    ],
]

pacific2024 = [
    [ # ソフトバンク
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 11, "l": 7, "d": 1, "r": 6},
        {"w": 15, "l": 8, "d": 1, "r": 1},
        {"w": 11, "l": 9, "d": 0, "r": 5},
        {"w": 10, "l": 6, "d": 1, "r": 8},
        {"w": 15, "l": 5, "d": 0, "r": 5},
        {"w": 12, "l": 6, "d": 0, "r": 0},
    ],
    [ # 日本ハム
        {"w": 7, "l": 11, "d": 1, "r": 6},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 17, "l": 6, "d": 1, "r": 1},
        {"w": 10, "l": 6, "d": 2, "r": 7},
        {"w": 9, "l": 10, "d": 1, "r": 5},
        {"w": 11, "l": 7, "d": 2, "r": 5},
        {"w": 7, "l": 10, "d": 1, "r": 0},
    ],
    [ # ロッテ
        {"w": 8, "l": 15, "d": 1, "r": 1},
        {"w": 6, "l": 17, "d": 1, "r": 1},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 9, "l": 6, "d": 1, "r": 9},
        {"w": 14, "l": 7, "d": 1, "r": 3},
        {"w": 16, "l": 1, "d": 0, "r": 8},
        {"w": 7, "l": 9, "d": 2, "r": 0},
    ],
    [ # 楽天
        {"w": 9, "l": 11, "d": 0, "r": 5},
        {"w": 6, "l": 10, "d": 2, "r": 7},
        {"w": 6, "l": 9, "d": 1, "r": 9},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 9, "l": 12, "d": 0, "r": 4},
        {"w": 13, "l": 10, "d": 0, "r": 2},
        {"w": 13, "l": 5, "d": 0, "r": 0},
    ],
    [ # オリックス
        {"w": 6, "l": 10, "d": 1, "r": 8},
        {"w": 10, "l": 9, "d": 1, "r": 5},
        {"w": 7, "l": 14, "d": 1, "r": 3},
        {"w": 12, "l": 9, "d": 0, "r": 4},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 10, "l": 11, "d": 0, "r": 4},
        {"w": 10, "l": 8, "d": 0, "r": 0},
    ],
    [ # 西武
        {"w": 5, "l": 15, "d": 0, "r": 5},
        {"w": 7, "l": 11, "d": 2, "r": 5},
        {"w": 1, "l": 16, "d": 0, "r": 8},
        {"w": 10, "l": 13, "d": 0, "r": 2},
        {"w": 11, "l": 10, "d": 0, "r": 4},
        {"w": 0, "l": 0, "d": 0, "r": 0},
        {"w": 4, "l": 14, "d": 0, "r": 0},
    ],
]

class MainTest(unittest.TestCase):
    def test_pacific(self):
        pacificResult = calculate.getResult(pacific2024)
        pacificOriginalData = '[{"max": "99/140", "now": "74/115", "min": "37/70", "win1": "17/27", "win2": "82/137", "win3": "73/129", "selfV": "81/137", "canSelfV": true, "lose1": "38/141", "lose2": "11/28", "lose3": "56/137", "win1Magic": 15, "win2Magic": 10, "win3Magic": 6, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"max": "17/27", "now": "61/111", "min": "61/135", "win1": "99/140", "win2": "82/137", "win3": "73/129", "selfV": "93/140", "canSelfV": false, "lose1": "38/141", "lose2": "11/28", "lose3": "56/137", "win1Magic": null, "win2Magic": 20, "win3Magic": 16, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"max": "82/137", "now": "12/23", "min": "60/137", "win1": "99/140", "win2": "17/27", "win3": "78/133", "selfV": "7/10", "canSelfV": false, "lose1": "38/141", "lose2": "11/28", "lose3": "56/137", "win1Magic": null, "win2Magic": null, "win3Magic": 21, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"max": "83/140", "now": "56/113", "min": "2/5", "win1": "99/140", "win2": "17/27", "win3": "82/137", "selfV": "47/70", "canSelfV": false, "lose1": "38/141", "lose2": "11/28", "lose3": "60/137", "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": null, "lose2Magic": null, "lose3Magic": -22}, {"max": "79/140", "now": "55/116", "min": "11/28", "win1": "99/140", "win2": "17/27", "win3": "82/137", "selfV": "13/20", "canSelfV": false, "lose1": "38/141", "lose2": "2/5", "lose3": "60/133", "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": null, "lose2Magic": -23, "lose3Magic": -16}, {"max": "62/141", "now": "38/117", "min": "38/141", "win1": "99/140", "win2": "17/27", "win3": "82/137", "selfV": "47/70", "canSelfV": false, "lose1": "11/28", "lose2": "56/137", "lose3": "60/133", "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": -7, "lose2Magic": -5, "lose3Magic": null}]'
        self.assertEqual(json.loads(pacificOriginalData), pacificResult)

    def test_central(self):
        centralResult = calculate.getResult(central2024)
        centralOriginalData = '[{"max": "15/23", "now": "31/55", "min": "31/69", "win1": "87/137", "win2": "81/137", "win3": "77/135", "selfV": "81/137", "canSelfV": true, "lose1": "47/139", "lose2": "25/67", "lose3": "57/140", "win1Magic": 26, "win2Magic": 20, "win3Magic": 17, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"max": "87/137", "now": "63/113", "min": "63/137", "win1": "15/23", "win2": "28/47", "win3": "77/135", "selfV": "14/23", "canSelfV": true, "lose1": "47/139", "lose2": "25/67", "lose3": "57/140", "win1Magic": null, "win2Magic": 19, "win3Magic": 16, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"max": "81/137", "now": "59/115", "min": "59/137", "win1": "15/23", "win2": "83/133", "win3": "82/139", "selfV": "29/46", "canSelfV": false, "lose1": "47/139", "lose2": "25/67", "lose3": "57/140", "win1Magic": null, "win2Magic": null, "win3Magic": 22, "lose1Magic": null, "lose2Magic": null, "lose3Magic": null}, {"max": "28/47", "now": "1/2", "min": "19/47", "win1": "15/23", "win2": "83/133", "win3": "81/137", "selfV": "14/23", "canSelfV": false, "lose1": "47/139", "lose2": "25/67", "lose3": "59/137", "win1Magic": null, "win2Magic": null, "win3Magic": 27, "lose1Magic": null, "lose2Magic": null, "lose3Magic": -24}, {"max": "73/135", "now": "25/56", "min": "10/27", "win1": "15/23", "win2": "83/133", "win3": "81/137", "selfV": "84/137", "canSelfV": false, "lose1": "47/139", "lose2": "19/47", "lose3": "61/138", "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": null, "lose2Magic": -19, "lose3Magic": -14}, {"max": "73/139", "now": "47/113", "min": "47/139", "win1": "15/23", "win2": "83/133", "win3": "81/137", "selfV": "83/138", "canSelfV": false, "lose1": "10/27", "lose2": "57/140", "lose3": "61/138", "win1Magic": null, "win2Magic": null, "win3Magic": null, "lose1Magic": -22, "lose2Magic": -17, "lose3Magic": -12}]'
        self.assertEqual(json.loads(centralOriginalData), centralResult)


if __name__ == "__main__":
    unittest.main()

