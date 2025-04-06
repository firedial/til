
MENZEN = 1
REACH = 2
CHANKAN = 3
RINSHAN = 4
HAITEI = 5
HOUTEI = 6
HAKU = 7
HATSU = 8
CHUN = 9
JIFUU = 10
BAHUU = 11
TANYAO = 12
IPEKO = 13
PINFU = 14
CHANTA = 15
ITTSU = 16
SANJUN = 17
DOUBLE = 18
SANDO = 19
SANKANTSU = 20
TOITOI = 21
SANANKO = 22
SHOSANGEN = 23
HONRO = 24
CHITOI = 25
JUNCHAN = 26
HONITSU = 27
RYANPEKO = 28
CHINITSU = 29
IPPATSU = 30
DORA = 31
AKADORA = 32
URADORA = 33

TENHO = 35
CHIHO = 36
DAISANGEN = 37
SUANKO = 38
TSUISO = 39
RYUISO = 40
CHINROTO = 41
KOKUSHI = 42
SHOSUSHI = 43
SUKANTSU = 44
CHUREN = 45
JUNCHUREN = 47
SUANKOTANKI = 48
KOKUSHIJUSAN = 49
DAISUSHI = 50

YAKUINFO = {
    MENZEN: {
        "name": "門前清自摸和",
    },
    REACH: {
        "name": "立直",
    },
    CHANKAN: {
        "name": "槍槓",
    },
    RINSHAN: {
        "name": "嶺上開花",
    },
    HAITEI: {
        "name": "海底撈月",
    },
    HOUTEI: {
        "name": "河底撈魚",
    },
    HAKU: {
        "name": "役牌白",
    },
    #...
    TENHO: {
        "name": "天和",
    },
    CHIHO: {
        "name": "地和",
    },
    DAISANGEN: {
        "name": "大三元",
    },
    SUANKO: {
        "name": "四暗刻",
    },
    TSUISO: {
        "name": "字一色",
    },
    RYUISO: {
        "name": "緑一色",
    },
    CHINROTO: {
        "name": "清老頭",
    },
    KOKUSHI: {
        "name": "国士無双",
    },
    SHOSUSHI: {
        "name": "小四喜",
    },
    SUKANTSU: {
        "name": "四槓子",
    },
    CHUREN: {
        "name": "九蓮宝燈",
    },
    JUNCHUREN: {
        "name": "純正九蓮宝燈",
    },
    SUANKOTANKI: {
        "name": "四暗刻単騎",
    },
    KOKUSHIJUSAN: {
        "name": "国士無双十三面待ち",
    },
    DAISUSHI: {
        "name": "大四喜",
    },
}

YAKUS = [
    MENZEN,
    REACH,
    CHANKAN,
    RINSHAN,
    HAITEI,
    HOUTEI,
    HAKU,
    HATSU,
    CHUN,
    JIFUU,
    BAHUU,
    TANYAO,
    IPEKO,
    PINFU,
    CHANTA,
    ITTSU,
    SANJUN,
    DOUBLE,
    SANDO,
    SANKANTSU,
    TOITOI,
    SANANKO,
    SHOSANGEN,
    HONRO,
    CHITOI,
    JUNCHAN,
    HONITSU,
    RYANPEKO,
    CHINITSU,
    IPPATSU,
    DORA,
    AKADORA,
    URADORA,
]
YAKUS = []

YAKUMANS = [
    TENHO,
    CHIHO,
    DAISANGEN,
    SUANKO,
    TSUISO,
    RYUISO,
    CHINROTO,
    KOKUSHI,
    SHOSUSHI,
    SUKANTSU,
    CHUREN,
    JUNCHUREN,
    SUANKOTANKI,
    KOKUSHIJUSAN,
    DAISUSHI,
]

CONDITIONS = {
    frozenset([TENHO]):
        {
            "need": [],
            "no": [CHIHO, SUKANTSU, CHUREN, KOKUSHI, SUANKO] + YAKUS,
        },
    frozenset([CHIHO]):
        {
            "need": [],
            "no": [TENHO, SUKANTSU] + YAKUS,
        },
    frozenset([DAISANGEN]):
        {
            "need": [],
            "no": [RYUISO, CHINROTO, KOKUSHI, SHOSUSHI, CHUREN, JUNCHUREN, KOKUSHIJUSAN, DAISUSHI] + YAKUS,
        },
    frozenset([TSUISO]):
        {
            "need": [],
            "no": [RYUISO, CHINROTO, KOKUSHI, CHUREN, JUNCHUREN, KOKUSHIJUSAN] + YAKUS,
        },
    frozenset([RYUISO]):
        {
            "need": [],
            "no": [DAISANGEN, TSUISO, CHINROTO, KOKUSHI, CHUREN, JUNCHUREN, KOKUSHIJUSAN, SHOSUSHI, DAISUSHI] + YAKUS,
        },
    frozenset([CHINROTO]):
        {
            "need": [],
            "no": [DAISANGEN, TSUISO, RYUISO, KOKUSHI, CHUREN, JUNCHUREN, KOKUSHIJUSAN, SHOSUSHI, DAISUSHI] + YAKUS,
        },
    frozenset([SUKANTSU]):
        {
            "need": [],
            "no": [TENHO, CHIHO, CHUREN, JUNCHUREN, KOKUSHI, KOKUSHIJUSAN] + YAKUS,
        },
    frozenset([SHOSUSHI]):
        {
            "need": [],
            "no": [DAISANGEN, CHINROTO, RYUISO, DAISUSHI, CHUREN, JUNCHUREN, KOKUSHI, KOKUSHIJUSAN] + YAKUS,
        },
    frozenset([DAISUSHI]):
        {
            "need": [],
            "no": [DAISANGEN, CHINROTO, RYUISO, SHOSUSHI, CHUREN, JUNCHUREN, KOKUSHI, KOKUSHIJUSAN] + YAKUS,
        },
    frozenset([SUANKO]):
        {
            "need": [],
            "no": [TENHO, SUANKOTANKI, KOKUSHI, CHUREN, JUNCHUREN, KOKUSHIJUSAN] + YAKUS,
        },
    frozenset([SUANKOTANKI]):
        {
            "need": [],
            "no": [SUANKO, KOKUSHI, CHUREN, JUNCHUREN, KOKUSHIJUSAN] + YAKUS,
        },
    frozenset([CHUREN]):
        {
            "need": [],
            "no": [TENHO, DAISANGEN, CHINROTO, TSUISO, RYUISO, SUKANTSU, SHOSUSHI, DAISUSHI, SUANKO, JUNCHUREN, KOKUSHI, KOKUSHIJUSAN] + YAKUS,
        },
    frozenset([JUNCHUREN]):
        {
            "need": [],
            "no": [DAISANGEN, CHINROTO, TSUISO, RYUISO, SUKANTSU, SHOSUSHI, DAISUSHI, SUANKO, CHUREN, KOKUSHI, KOKUSHIJUSAN] + YAKUS,
        },
    frozenset([KOKUSHI]):
        {
            "need": [],
            "no": [TENHO, DAISANGEN, CHINROTO, TSUISO, RYUISO, SUKANTSU, SHOSUSHI, DAISUSHI, SUANKO, CHUREN, JUNCHUREN, KOKUSHIJUSAN] + YAKUS,
        },
    frozenset([KOKUSHIJUSAN]):
        {
            "need": [],
            "no": [DAISANGEN, CHINROTO, TSUISO, RYUISO, SUKANTSU, SHOSUSHI, DAISUSHI, SUANKO, CHUREN, JUNCHUREN, KOKUSHI] + YAKUS,
        },
    frozenset([CHINROTO, TENHO]):
        {
            "need": [SUANKOTANKI],
            "no": [],
        },
    frozenset([CHINROTO, CHIHO]):
        {
            "need": [SUANKO, SUANKOTANKI],
            "no": [],
        },
    frozenset([TSUISO, TENHO]):
        {
            "need": [SUANKOTANKI],
            "no": [],
        },
    frozenset([TSUISO, CHIHO]):
        {
            "need": [SUANKO, SUANKOTANKI],
            "no": [],
        },
    frozenset([DAISUSHI, TENHO]):
        {
            "need": [SUANKOTANKI],
            "no": [],
        },
    frozenset([DAISUSHI, CHIHO]):
        {
            "need": [SUANKO, SUANKOTANKI],
            "no": [],
        },
}


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


c = {i: 0 for i in YAKUMANS}
result = set()
search(c)

lastResult = set()
remove = set()
# need 条件での除去
for r in result:
    if len(r) == 0:
        remove.add(r)
    for key, condition in CONDITIONS.items():
        if key <= r:
            if len(condition["need"]) == 0:
                continue
            for yaku in condition["need"]:
                if frozenset([yaku]) <= r:
                    break
            else:
                remove.add(r)




lastResult = result - remove

for p in lastResult:
    for yaku in p:
        print(YAKUINFO[yaku]["name"] + ",", end="")
    print()

print(len(lastResult))

# print(result)
# print(len(result))
# print(remove)
# print(len(lastResult))
# print(lastResult)

# print(c)
# print(CONDITIONS)
# print(len(YAKUMANS))

