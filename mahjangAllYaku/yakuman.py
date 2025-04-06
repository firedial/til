import yaku

YAKUMANS = list(dict(filter(lambda x: x[1]["kind"] == yaku.YAKU_KIND_YAKUMAN, yaku.YAKUINFO.items())).keys())

IMPOSSIBLE_COMBINE = frozenset([
    frozenset([yaku.TENHO, yaku.CHIHO]),
    frozenset([yaku.TENHO, yaku.SUKANTSU]),
    frozenset([yaku.TENHO, yaku.SUANKO]),
    frozenset([yaku.TENHO, yaku.CHUREN]),
    frozenset([yaku.TENHO, yaku.KOKUSHI]),
    frozenset([yaku.CHIHO, yaku.SUKANTSU]),
    frozenset([yaku.DAISANGEN, yaku.CHINROTO]),
    frozenset([yaku.DAISANGEN, yaku.RYUISO]),
    frozenset([yaku.DAISANGEN, yaku.SHOSUSHI]),
    frozenset([yaku.DAISANGEN, yaku.DAISUSHI]),
    frozenset([yaku.DAISANGEN, yaku.CHUREN]),
    frozenset([yaku.DAISANGEN, yaku.JUNCHUREN]),
    frozenset([yaku.DAISANGEN, yaku.KOKUSHI]),
    frozenset([yaku.DAISANGEN, yaku.KOKUSHIJUSAN]),
    frozenset([yaku.CHINROTO, yaku.TSUISO]),
    frozenset([yaku.CHINROTO, yaku.RYUISO]),
    frozenset([yaku.CHINROTO, yaku.SHOSUSHI]),
    frozenset([yaku.CHINROTO, yaku.DAISUSHI]),
    frozenset([yaku.CHINROTO, yaku.CHUREN]),
    frozenset([yaku.CHINROTO, yaku.JUNCHUREN]),
    frozenset([yaku.CHINROTO, yaku.KOKUSHI]),
    frozenset([yaku.CHINROTO, yaku.KOKUSHIJUSAN]),
    frozenset([yaku.TSUISO, yaku.RYUISO]),
    frozenset([yaku.TSUISO, yaku.CHUREN]),
    frozenset([yaku.TSUISO, yaku.JUNCHUREN]),
    frozenset([yaku.TSUISO, yaku.KOKUSHI]),
    frozenset([yaku.TSUISO, yaku.KOKUSHIJUSAN]),
    frozenset([yaku.RYUISO, yaku.SHOSUSHI]),
    frozenset([yaku.RYUISO, yaku.DAISUSHI]),
    frozenset([yaku.RYUISO, yaku.CHUREN]),
    frozenset([yaku.RYUISO, yaku.JUNCHUREN]),
    frozenset([yaku.RYUISO, yaku.KOKUSHI]),
    frozenset([yaku.RYUISO, yaku.KOKUSHIJUSAN]),
    frozenset([yaku.SUKANTSU, yaku.CHUREN]),
    frozenset([yaku.SUKANTSU, yaku.JUNCHUREN]),
    frozenset([yaku.SUKANTSU, yaku.KOKUSHI]),
    frozenset([yaku.SUKANTSU, yaku.KOKUSHIJUSAN]),
    frozenset([yaku.SHOSUSHI, yaku.DAISUSHI]),
    frozenset([yaku.SHOSUSHI, yaku.CHUREN]),
    frozenset([yaku.SHOSUSHI, yaku.JUNCHUREN]),
    frozenset([yaku.SHOSUSHI, yaku.KOKUSHI]),
    frozenset([yaku.SHOSUSHI, yaku.KOKUSHIJUSAN]),
    frozenset([yaku.DAISUSHI, yaku.CHUREN]),
    frozenset([yaku.DAISUSHI, yaku.JUNCHUREN]),
    frozenset([yaku.DAISUSHI, yaku.KOKUSHI]),
    frozenset([yaku.DAISUSHI, yaku.KOKUSHIJUSAN]),
    frozenset([yaku.SUANKO, yaku.SUANKOTANKI]),
    frozenset([yaku.SUANKO, yaku.CHUREN]),
    frozenset([yaku.SUANKO, yaku.JUNCHUREN]),
    frozenset([yaku.SUANKO, yaku.KOKUSHI]),
    frozenset([yaku.SUANKO, yaku.KOKUSHIJUSAN]),
    frozenset([yaku.SUANKOTANKI, yaku.CHUREN]),
    frozenset([yaku.SUANKOTANKI, yaku.JUNCHUREN]),
    frozenset([yaku.SUANKOTANKI, yaku.KOKUSHI]),
    frozenset([yaku.SUANKOTANKI, yaku.KOKUSHIJUSAN]),
    frozenset([yaku.CHUREN, yaku.JUNCHUREN]),
    frozenset([yaku.CHUREN, yaku.KOKUSHI]),
    frozenset([yaku.CHUREN, yaku.KOKUSHIJUSAN]),
    frozenset([yaku.JUNCHUREN, yaku.KOKUSHI]),
    frozenset([yaku.JUNCHUREN, yaku.KOKUSHIJUSAN]),
    frozenset([yaku.KOKUSHI, yaku.KOKUSHIJUSAN]),
])

CONDITIONS = {
    frozenset([yaku]): {
        "no": list(
            map(
                lambda y: tuple((y - frozenset([yaku])))[0],
                filter(
                    lambda x: frozenset([yaku]) <= x,
                    IMPOSSIBLE_COMBINE
                )
            )
        )
    }
    for yaku in YAKUMANS
}

YAKU_NONE = 0 # 役未決定
YAKU_HAVE = 1 # 役に持つ
YAKU_NOT_HAVE = -1 # 役に持たない

def check(c):
    filtered = frozenset(dict(filter(lambda x: x[1] == 1, c.items())).keys())
    for key, condition in CONDITIONS.items():
        if key <= filtered:
            for yaku in condition["no"]:
                if c[yaku] == 1:
                    return -1
                else:
                    c[yaku] = -1

def search(c):
    rc = check(c)
    # 矛盾おきたとき
    if rc == -1:
        return

    # まだ未確定の役
    filtered = list(filter(lambda x: x[1] == 0, c.items()))
    if len(filtered) == 0:
        result.add(frozenset(map(lambda y: y[0], filter(lambda x: x[1] == 1, c.items()))))
        return

    i = filtered[0][0]

    nextC = c.copy()
    nextC[i] = 1
    search(nextC)

    nextC = c.copy()
    nextC[i] = -1
    search(nextC)


c = {i: YAKU_NONE for i in YAKUMANS}
result = set()
search(c)

lastResult = set()
for r in result:
    # 役なし
    if len(r) == 0:
        continue

    # 清老頭と天和が複合していた場合は、四暗刻単騎に複合している
    if frozenset([yaku.CHINROTO, yaku.TENHO]) <= r:
        if yaku.SUANKOTANKI not in r:
            # 含んでいなかったらカウントしない
            continue

    # 清老頭と地和が複合していた場合は、四暗刻単騎か四暗刻に複合している
    if frozenset([yaku.CHINROTO, yaku.CHIHO]) <= r:
        if yaku.SUANKOTANKI not in r and yaku.SUANKOTANKI not in r:
            # 含んでいなかったらカウントしない
            continue

    # 字一色と天和が複合していた場合は、四暗刻単騎に複合している
    if frozenset([yaku.TSUISO, yaku.TENHO]) <= r:
        if yaku.SUANKOTANKI not in r:
            # 含んでいなかったらカウントしない
            continue

    # 字一色と地和が複合していた場合は、四暗刻単騎か四暗刻に複合している
    if frozenset([yaku.TSUISO, yaku.CHIHO]) <= r:
        if yaku.SUANKOTANKI not in r and yaku.SUANKOTANKI not in r:
            # 含んでいなかったらカウントしない
            continue

    # 大四喜と天和が複合していた場合は、四暗刻単騎に複合している
    if frozenset([yaku.DAISUSHI, yaku.TENHO]) <= r:
        if yaku.SUANKOTANKI not in r:
            # 含んでいなかったらカウントしない
            continue

    # 大四喜と地和が複合していた場合は、四暗刻単騎か四暗刻に複合している
    if frozenset([yaku.DAISUSHI, yaku.CHIHO]) <= r:
        if yaku.SUANKOTANKI not in r and yaku.SUANKOTANKI not in r:
            # 含んでいなかったらカウントしない
            continue

    lastResult.add(r)

for p in lastResult:
    for y in p:
        print(yaku.YAKUINFO[y]["name"] + ",", end="")
    print()

print(len(lastResult))

import csv
real = set()
with open('data.csv') as f:
    csvreader = csv.reader(f)
    for i, row in enumerate(csvreader):
        s = (row[0][2:-1] + "0")[::-1]
        y = set()
        for bi, b in enumerate(s):
            if bi >= 35 and bi <= 50 and bi != 46 and b == "1":
                y.add(bi)

        if len(y) != 0:
            real.add(frozenset(y))


for p in lastResult - real:
    for y in p:
        print(yaku.YAKUINFO[y]["name"] + ",", end="")
    print()

print(len(lastResult - real))
