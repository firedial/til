import yaku

NORMAL_YAKUS = list(dict(filter(lambda x: x[1]["kind"] == yaku.YAKU_KIND_YAKU, yaku.YAKUINFO.items())).keys())

IMPOSSIBLE_COMBINE = frozenset([
    frozenset([yaku.MENZEN, yaku.CHANKAN]),
    frozenset([yaku.MENZEN, yaku.HOUTEI]),
    frozenset([yaku.MENZEN, yaku.TOITOI]),
    frozenset([yaku.REACH, yaku.DOUBLE]),
    frozenset([yaku.CHANKAN, yaku.RINSHAN]),
    frozenset([yaku.CHANKAN, yaku.HAITEI]),
    frozenset([yaku.CHANKAN, yaku.HOUTEI]),
    frozenset([yaku.CHANKAN, yaku.TOITOI]),
    frozenset([yaku.CHANKAN, yaku.CHITOI]),
    frozenset([yaku.CHANKAN, yaku.RYANPEKO]),
    frozenset([yaku.RINSHAN, yaku.HAITEI]),
    frozenset([yaku.RINSHAN, yaku.HOUTEI]),
    frozenset([yaku.RINSHAN, yaku.CHITOI]),
    frozenset([yaku.RINSHAN, yaku.RYANPEKO]),
    frozenset([yaku.RINSHAN, yaku.IPPATSU]),
    frozenset([yaku.HAITEI, yaku.HOUTEI]),
    frozenset([yaku.HAKU, yaku.TANYAO]),
    frozenset([yaku.HAKU, yaku.PINFU]),
    frozenset([yaku.HAKU, yaku.CHITOI]),
    frozenset([yaku.HAKU, yaku.JUNCHAN]),
    frozenset([yaku.HAKU, yaku.RYANPEKO]),
    frozenset([yaku.HAKU, yaku.CHINITSU]),
    frozenset([yaku.HATSU, yaku.TANYAO]),
    frozenset([yaku.HATSU, yaku.PINFU]),
    frozenset([yaku.HATSU, yaku.CHITOI]),
    frozenset([yaku.HATSU, yaku.JUNCHAN]),
    frozenset([yaku.HATSU, yaku.RYANPEKO]),
    frozenset([yaku.HATSU, yaku.CHINITSU]),
    frozenset([yaku.CHUN, yaku.TANYAO]),
    frozenset([yaku.CHUN, yaku.PINFU]),
    frozenset([yaku.CHUN, yaku.CHITOI]),
    frozenset([yaku.CHUN, yaku.JUNCHAN]),
    frozenset([yaku.CHUN, yaku.RYANPEKO]),
    frozenset([yaku.CHUN, yaku.CHINITSU]),
    frozenset([yaku.JIFUU, yaku.TANYAO]),
    frozenset([yaku.JIFUU, yaku.PINFU]),
    frozenset([yaku.JIFUU, yaku.CHITOI]),
    frozenset([yaku.JIFUU, yaku.JUNCHAN]),
    frozenset([yaku.JIFUU, yaku.RYANPEKO]),
    frozenset([yaku.JIFUU, yaku.CHINITSU]),
    frozenset([yaku.BAHUU, yaku.TANYAO]),
    frozenset([yaku.BAHUU, yaku.PINFU]),
    frozenset([yaku.BAHUU, yaku.CHITOI]),
    frozenset([yaku.BAHUU, yaku.JUNCHAN]),
    frozenset([yaku.BAHUU, yaku.RYANPEKO]),
    frozenset([yaku.BAHUU, yaku.CHINITSU]),
    frozenset([yaku.TANYAO, yaku.CHANTA]),
    frozenset([yaku.TANYAO, yaku.ITTSU]),
    frozenset([yaku.TANYAO, yaku.SHOSANGEN]),
    frozenset([yaku.TANYAO, yaku.HONRO]),
    frozenset([yaku.TANYAO, yaku.JUNCHAN]),
    frozenset([yaku.TANYAO, yaku.HONITSU]),
    frozenset([yaku.IPEKO, yaku.SANDO]),
    frozenset([yaku.IPEKO, yaku.SANKANTSU]),
    frozenset([yaku.IPEKO, yaku.TOITOI]),
    frozenset([yaku.IPEKO, yaku.SANANKO]),
    frozenset([yaku.IPEKO, yaku.HONRO]),
    frozenset([yaku.IPEKO, yaku.CHITOI]),
    frozenset([yaku.IPEKO, yaku.RYANPEKO]),
    frozenset([yaku.PINFU, yaku.SANDO]),
    frozenset([yaku.PINFU, yaku.SANKANTSU]),
    frozenset([yaku.PINFU, yaku.TOITOI]),
    frozenset([yaku.PINFU, yaku.SANANKO]),
    frozenset([yaku.PINFU, yaku.SHOSANGEN]),
    frozenset([yaku.PINFU, yaku.HONRO]),
    frozenset([yaku.PINFU, yaku.CHITOI]),
    frozenset([yaku.CHANTA, yaku.ITTSU]),
    frozenset([yaku.CHANTA, yaku.TOITOI]),
    frozenset([yaku.CHANTA, yaku.HONRO]),
    frozenset([yaku.CHANTA, yaku.CHITOI]),
    frozenset([yaku.CHANTA, yaku.JUNCHAN]),
    frozenset([yaku.CHANTA, yaku.CHINITSU]),
    frozenset([yaku.CHANTA, yaku.AKADORA]),
    frozenset([yaku.ITTSU, yaku.SANJUN]),
    frozenset([yaku.ITTSU, yaku.SANDO]),
    frozenset([yaku.ITTSU, yaku.SANKANTSU]),
    frozenset([yaku.ITTSU, yaku.TOITOI]),
    frozenset([yaku.ITTSU, yaku.SANANKO]),
    frozenset([yaku.ITTSU, yaku.SHOSANGEN]),
    frozenset([yaku.ITTSU, yaku.HONRO]),
    frozenset([yaku.ITTSU, yaku.CHITOI]),
    frozenset([yaku.ITTSU, yaku.JUNCHAN]),
    frozenset([yaku.ITTSU, yaku.RYANPEKO]),
    frozenset([yaku.SANJUN, yaku.SANDO]),
    frozenset([yaku.SANJUN, yaku.SANKANTSU]),
    frozenset([yaku.SANJUN, yaku.TOITOI]),
    frozenset([yaku.SANJUN, yaku.SANANKO]),
    frozenset([yaku.SANJUN, yaku.SHOSANGEN]),
    frozenset([yaku.SANJUN, yaku.HONRO]),
    frozenset([yaku.SANJUN, yaku.CHITOI]),
    frozenset([yaku.SANJUN, yaku.HONITSU]),
    frozenset([yaku.SANJUN, yaku.RYANPEKO]),
    frozenset([yaku.SANJUN, yaku.CHINITSU]),
    frozenset([yaku.SANDO, yaku.SHOSANGEN]),
    frozenset([yaku.SANDO, yaku.CHITOI]),
    frozenset([yaku.SANDO, yaku.HONITSU]),
    frozenset([yaku.SANDO, yaku.RYANPEKO]),
    frozenset([yaku.SANDO, yaku.CHINITSU]),
    frozenset([yaku.SANKANTSU, yaku.CHITOI]),
    frozenset([yaku.SANKANTSU, yaku.RYANPEKO]),
    frozenset([yaku.TOITOI, yaku.CHITOI]),
    frozenset([yaku.TOITOI, yaku.JUNCHAN]),
    frozenset([yaku.TOITOI, yaku.RYANPEKO]),
    frozenset([yaku.SANANKO, yaku.CHITOI]),
    frozenset([yaku.SANANKO, yaku.RYANPEKO]),
    frozenset([yaku.SHOSANGEN, yaku.CHITOI]),
    frozenset([yaku.SHOSANGEN, yaku.JUNCHAN]),
    frozenset([yaku.SHOSANGEN, yaku.RYANPEKO]),
    frozenset([yaku.SHOSANGEN, yaku.CHINITSU]),
    frozenset([yaku.HONRO, yaku.JUNCHAN]),
    frozenset([yaku.HONRO, yaku.RYANPEKO]),
    frozenset([yaku.HONRO, yaku.CHINITSU]),
    frozenset([yaku.HONRO, yaku.AKADORA]),
    frozenset([yaku.CHITOI, yaku.JUNCHAN]),
    frozenset([yaku.CHITOI, yaku.RYANPEKO]),
    frozenset([yaku.JUNCHAN, yaku.HONITSU]),
    frozenset([yaku.JUNCHAN, yaku.AKADORA]),
    frozenset([yaku.HONITSU, yaku.CHINITSU]),
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
    for yaku in NORMAL_YAKUS
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


def trans(c):
    if yaku.HAKU in c and yaku.HATSU not in c and yaku.CHUN not in c:
        pass
    elif yaku.HAKU not in c and yaku.HATSU in c and yaku.CHUN not in c:
        c.remove(yaku.HATSU)
        c.add(yaku.HAKU)
    elif yaku.HAKU not in c and yaku.HATSU not in c and yaku.CHUN in c:
        c.remove(yaku.CHUN)
        c.add(yaku.HAKU)
    elif yaku.HAKU in c and yaku.HATSU in c and yaku.CHUN not in c:
        pass
    elif yaku.HAKU in c and yaku.HATSU not in c and yaku.CHUN in c:
        c.remove(yaku.CHUN)
        c.add(yaku.HATSU)
    elif yaku.HAKU not in c and yaku.HATSU in c and yaku.CHUN in c:
        c.remove(yaku.CHUN)
        c.add(yaku.HAKU)

    if yaku.JIFUU in c and yaku.BAHUU not in c:
        pass
    if yaku.JIFUU not in c and yaku.BAHUU in c:
        c.remove(yaku.BAHUU)
        c.add(yaku.JIFUU)
    if yaku.JIFUU in c and yaku.BAHUU in c:
        c.remove(yaku.BAHUU)

    if yaku.DORA in c:
        c.remove(yaku.DORA)

    if yaku.URADORA in c:
        c.remove(yaku.URADORA)

    # if yaku.AKADORA in c:
    #     c.remove(yaku.AKADORA)

    return c

c = {i: YAKU_NONE for i in NORMAL_YAKUS}
result = set()
search(c)

lastResult = set()
for r in result:
    # 役なし
    if len(r) == 0:
        continue

    # ドラと赤ドラだけ
    if r <= frozenset([yaku.DORA, yaku.AKADORA]):
        # カウントしない
        continue

    # 三元牌の全てあったら大三元になるのでカウントしない
    # @todo 何故かリストに入ってきちゃっている
    if frozenset([yaku.HAKU, yaku.HATSU, yaku.CHUN]) <= r:
        # カウントしない
        continue

    # 立直、嶺上開花なら、門前清自摸和になるのでカウントしない
    if frozenset([yaku.REACH, yaku.RINSHAN]) <= r:
        if yaku.MENZEN not in r:
            # カウントしない
            continue

    # ダブル立直、嶺上開花なら、門前清自摸和になるのでカウントしない
    if frozenset([yaku.DOUBLE, yaku.RINSHAN]) <= r:
        if yaku.MENZEN not in r:
            # カウントしない
            continue

    # 立直、海底撈月なら、門前清自摸和になるのでカウントしない
    if frozenset([yaku.REACH, yaku.HAITEI]) <= r:
        if yaku.MENZEN not in r:
            # カウントしない
            continue

    # ダブル立直、海底撈月なら、門前清自摸和になるのでカウントしない
    if frozenset([yaku.DOUBLE, yaku.HAITEI]) <= r:
        if yaku.MENZEN not in r:
            # カウントしない
            continue

    # 純全帯幺九、対々和なら、清老頭になるのでカウントしない
    # 上の IMPOSSIBLE_COMBINES ではじいていた
    # if frozenset([yaku.JUNCHAN, yaku.TOITOI]) <= r:
    #     # カウントしない
    #     continue

    # 裏ドラがある場合は、立直かダブル立直をしている
    if frozenset([yaku.URADORA]) <= r:
        if yaku.REACH not in r and yaku.DOUBLE not in r:
            # カウントしない
            continue

    # 一発がある場合は、立直かダブル立直をしている
    if frozenset([yaku.IPPATSU]) <= r:
        if yaku.REACH not in r and yaku.DOUBLE not in r:
            # カウントしない
            continue

    # 立直と三槓子がある場合は、三暗刻がついている
    if frozenset([yaku.REACH, yaku.SANKANTSU]) <= r:
        if yaku.SANANKO not in r:
            # カウントしない
            continue

    # ダブル立直と三槓子がある場合は、三暗刻がついている
    if frozenset([yaku.DOUBLE, yaku.SANKANTSU]) <= r:
        if yaku.SANANKO not in r:
            # カウントしない
            continue

    # 立直と対々和がある場合は、三暗刻がついている
    if frozenset([yaku.REACH, yaku.TOITOI]) <= r:
        if yaku.SANANKO not in r:
            # カウントしない
            continue

    # ダブル立直と対々和がある場合は、三暗刻がついている
    if frozenset([yaku.DOUBLE, yaku.TOITOI]) <= r:
        if yaku.SANANKO not in r:
            # カウントしない
            continue

    sangenCount = len(list(filter(lambda x: x in [yaku.HAKU, yaku.HATSU, yaku.CHUN], list(r))))
    hasKaze = len(list(filter(lambda x: x in [yaku.JIFUU, yaku.BAHUU], list(r)))) != 0
    yakuhaiCount = sangenCount + (1 if hasKaze else 0) # ダブ東とダブ南の考慮
    # 三色同順がある場合は、役牌は最大1つまで
    if frozenset([yaku.SANJUN]) <= r:
        if yakuhaiCount > 1:
            # カウントしない
            continue

    # 三色同刻がある場合は、役牌は最大1つまで
    if frozenset([yaku.SANDO]) <= r:
        if yakuhaiCount > 1:
            # カウントしない
            continue

    # 三色同刻と役牌がある場合は、対々和がついている
    if frozenset([yaku.SANDO]) <= r and yakuhaiCount == 1:
        if yaku.TOITOI not in r:
            # カウントしない
            continue

    # 三色同刻と役牌と門前清自摸和がある場合は、四暗刻か四暗刻単騎になる
    if frozenset([yaku.SANDO, yaku.MENZEN]) <= r and yakuhaiCount == 1:
        # カウントしない
        continue

    # 三色同刻と門前清自摸和がある場合は、三暗刻になる
    if frozenset([yaku.SANDO, yaku.MENZEN]) <= r:
        if yaku.SANANKO not in r:
            # カウントしない
            continue

    # 立直と三色同刻と役牌がある場合は、三暗刻になる
    # 立直と対々和となって、別条件で三暗刻判定になっている
    # if frozenset([yaku.REACH, yaku.SANDO]) <= r and yakuhaiCount == 1:
    #     if yaku.SANANKO not in r:
    #         # カウントしない
    #         continue

    # 一気通貫がある場合は、役牌は最大1つまで
    if frozenset([yaku.ITTSU]) <= r:
        if yakuhaiCount > 1:
            # カウントしない
            continue

    # 一盃口がある場合は、役牌は最大2つまで
    if frozenset([yaku.IPEKO]) <= r:
        if yakuhaiCount > 2:
            # カウントしない
            continue

    # 一気通貫と一盃口がある場合は、役牌はない
    if frozenset([yaku.ITTSU, yaku.IPEKO]) <= r:
        if yakuhaiCount > 0:
            # カウントしない
            continue

    # 三色同順と一盃口がある場合は、役牌はない
    if frozenset([yaku.SANJUN, yaku.IPEKO]) <= r:
        if yakuhaiCount > 0:
            # カウントしない
            continue

    # 役牌4つある場合は、対々和と混一色が確定する(雀頭が字牌だと字一色になるので数牌)
    # 今の判定方法だと、三元牌全部と風牌になるので大三元確定する
    # if yakuhaiCount == 4:
    #     if not frozenset([yaku.HONITSU]) <= r:
    #         # カウントしない
    #         continue

    # 小三元がある場合は、三元牌の2つが役牌になっている
    if frozenset([yaku.SHOSANGEN]) <= r:
        if not frozenset([yaku.HAKU, yaku.HATSU]) <= r and not frozenset([yaku.HATSU, yaku.CHUN]) <= r and not frozenset([yaku.CHUN, yaku.HAKU]) <= r:
            # カウントしない
            continue

    # 混老頭がある場合は、対々和か七対子になっている
    if frozenset([yaku.HONRO]) <= r:
        if yaku.TOITOI not in r and yaku.CHITOI not in r:
            # カウントしない
            continue

    # 七対子、清一色、断幺九の場合は、二盃口がつくのでカウントしない
    if frozenset([yaku.CHITOI, yaku.CHINITSU, yaku.TANYAO]) <= r:
        # カウントしない
        continue

    # ダブル立直の場合、海底撈月か河底撈魚と一発は同時に起こらない
    if frozenset([yaku.DOUBLE, yaku.IPPATSU, yaku.HAITEI]) <= r:
        # カウントしない
        continue
    if frozenset([yaku.DOUBLE, yaku.IPPATSU, yaku.HOUTEI]) <= r:
        # カウントしない
        continue

    # ダブル立直の場合、一発と三槓子は同時に起こらない
    if frozenset([yaku.DOUBLE, yaku.IPPATSU, yaku.SANKANTSU]) <= r:
        # カウントしない
        continue

    # 小三元に風牌がついていた場合、混一色が必ずつく
    if frozenset([yaku.SHOSANGEN, yaku.JIFUU]) <= r or frozenset([yaku.SHOSANGEN, yaku.BAHUU]) <= r:
        if yaku.HONITSU not in r:
            # カウントしない
            continue

    # 純全帯幺九と清一色と三暗刻は不可能
    if frozenset([yaku.JUNCHAN, yaku.CHINITSU, yaku.SANANKO]) <= r:
        # カウントしない
        continue

    # 純全帯幺九と清一色と三槓子は不可能
    if frozenset([yaku.JUNCHAN, yaku.CHINITSU, yaku.SANKANTSU]) <= r:
        # カウントしない
        continue

    # 三色同順と一盃口と嶺上開花は同時にできない
    if frozenset([yaku.SANJUN, yaku.IPEKO, yaku.RINSHAN]) <= r:
        # カウントしない
        continue

    # 一気通貫と一盃口と嶺上開花は同時にできない
    if frozenset([yaku.ITTSU, yaku.IPEKO, yaku.RINSHAN]) <= r:
        # カウントしない
        continue

    # 門前清自摸和と役牌3つあれば三暗刻になる
    if frozenset([yaku.MENZEN]) <= r and yakuhaiCount == 3:
        if yaku.SANANKO not in r:
            # カウントしない
            continue

    # 立直と役牌4つあれば三暗刻になる
    if frozenset([yaku.REACH]) <= r and yakuhaiCount == 4:
        if yaku.SANANKO not in r:
            # カウントしない
            continue

    # 槍槓と一盃口と役牌2つは同時に成り立たない
    if frozenset([yaku.CHANKAN, yaku.IPEKO]) <= r and yakuhaiCount == 2:
        # カウントしない
        continue

    # 平和と清一色と純全帯幺九があれば一盃口か二盃口が必ずつく
    if frozenset([yaku.PINFU, yaku.CHINITSU, yaku.JUNCHAN]) <= r:
        if yaku.IPEKO not in r and yaku.RYANPEKO not in r:
            # カウントしない
            continue

    # 平和と混一色と純全帯幺九があれば一盃口か二盃口が必ずつく
    if frozenset([yaku.PINFU, yaku.HONITSU, yaku.JUNCHAN]) <= r:
        if yaku.IPEKO not in r and yaku.RYANPEKO not in r:
            # カウントしない
            continue

    # 門前清自摸和と三槓子つあれば三暗刻になる
    if frozenset([yaku.MENZEN, yaku.SANKANTSU]) <= r:
        if yaku.SANANKO not in r:
            # カウントしない
            continue

    # ダブル立直と槍槓と一発は同時に発生しない
    if frozenset([yaku.DOUBLE, yaku.CHANKAN, yaku.IPPATSU]) <= r:
        # カウントしない
        continue

    # 小三元と一盃口がある場合は混一色がつく
    if frozenset([yaku.SHOSANGEN, yaku.IPEKO]) <= r:
        if yaku.HONITSU not in r:
            # カウントしない
            continue

    # # 立直と門前清自摸和と三色同刻あれば三暗刻になる
    # if frozenset([yaku.REACH, yaku.MENZEN, yaku.SANDO]) <= r:
    #     if yaku.SANANKO not in r:
    #         # カウントしない
    #         continue

    lastResult.add(frozenset(trans(set(r))))

# for p in lastResult:
#     for y in p:
#         print(yaku.YAKUINFO[y]["name"] + ",", end="")
#     print()

print(len(lastResult))


import csv
real = set()
with open('data.csv') as f:
    csvreader = csv.reader(f)
    for i, row in enumerate(csvreader):
        s = (row[0][2:-1] + "0")[::-1]
        y = set()
        for bi, b in enumerate(s):
            if bi <= 33 and b == "1":
                y.add(bi)

        if len(y) != 0:
            real.add(frozenset(trans(y)))


for p in lastResult - real:
    if yaku.SANKANTSU in p:
        continue
    if yaku.IPPATSU in p:
        continue
    if yaku.RINSHAN in p:
        continue
    if yaku.HOUTEI in p:
        continue
    if yaku.HAITEI in p:
        continue
    if yaku.DORA in p:
        continue
    if yaku.URADORA in p:
        continue
    if yaku.CHANKAN in p:
        continue
    if yaku.SANDO in p:
        continue
    if yaku.DOUBLE in p:
        continue
    if yaku.RYANPEKO in p:
        continue
    if yaku.REACH in p:
        continue
    if yaku.MENZEN in p:
        continue
    if yaku.AKADORA in p:
        continue
    if yaku.SHOSANGEN in p:
        continue

    for y in p:
        print(yaku.YAKUINFO[y]["name"] + ",", end="")
    print()

print(len(lastResult))
print(len(lastResult - real))
print(len(real - lastResult))

