import yaku

NORMAL_YAKUS = list(dict(filter(lambda x: x[1]["kind"] == yaku.YAKU_KIND_YAKU, yaku.YAKUINFO.items())).keys())

IMPOSSIBLE_COMBINE = frozenset([
    frozenset([yaku.MENZEN, yaku.CHANKAN]),
    frozenset([yaku.MENZEN, yaku.HOUTEI]),
    frozenset([yaku.REACH, yaku.DOUBLE]),
    frozenset([yaku.CHANKAN, yaku.RINSHAN]),
    frozenset([yaku.CHANKAN, yaku.HAITEI]),
    frozenset([yaku.CHANKAN, yaku.HOUTEI]),
    frozenset([yaku.RINSHAN, yaku.HAITEI]),
    frozenset([yaku.RINSHAN, yaku.HOUTEI]),
    frozenset([yaku.RINSHAN, yaku.CHITOI]),
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


c = {i: YAKU_NONE for i in NORMAL_YAKUS}
result = set()
search(c)

lastResult = set()
for r in result:
    # 役なし
    if len(r) == 0:
        continue

    # 三元牌の全てあったら大三元になるのでカウントしない
    if frozenset([yaku.HAKU, yaku.HATSU, yaku.CHUN]) <= r:
        # カウントしない
        continue

    # 立直、門前清自摸和、対々和なら、四暗刻か四暗刻単騎になるのでカウントしない
    if frozenset([yaku.REACH, yaku.MENZEN, yaku.TOITOI]) <= r:
        # カウントしない
        continue

    # 純全帯幺九、対々和なら、清老頭になるのでカウントしない
    # 上の IMPOSSIBLE_COMBINES ではじいていた
    # if frozenset([yaku.JUNCHAN, yaku.TOITOI]) <= r:
    #     # カウントしない
    #     continue

    # 裏ドラがある場合は、立直をしている
    if frozenset([yaku.URADORA]) <= r:
        if yaku.REACH not in r:
            # カウントしない
            continue

    # 一発がある場合は、立直をしている
    if frozenset([yaku.IPPATSU]) <= r:
        if yaku.REACH not in r:
            # カウントしない
            continue

    # 立直と三槓子がある場合は、三暗刻がついている
    if frozenset([yaku.REACH, yaku.SANKANTSU]) <= r:
        if yaku.SANANKO not in r:
            # カウントしない
            continue

    yakuhaiCount = len(list(filter(lambda x: x in [yaku.HAKU, yaku.HATSU, yaku.CHUN, yaku.JIFUU, yaku.BAHUU], list(r))))
    # 三色同順がある場合は、役牌は最大2つまで
    if frozenset([yaku.SANJUN]) <= r:
        if yakuhaiCount > 2:
            # カウントしない
            continue

    # 三色同刻がある場合は、役牌は最大2つまで
    if frozenset([yaku.SANJUN]) <= r:
        if yakuhaiCount > 2:
            # カウントしない
            continue

    # 一気通貫がある場合は、役牌は最大1つまで
    if frozenset([yaku.SANJUN]) <= r:
        if yakuhaiCount > 1:
            # カウントしない
            continue

    # 役牌4つある場合は、対々和と混一色が確定する(雀頭が字牌だと字一色になるので数牌)
    if yakuhaiCount == 4:
        if not frozenset([yaku.TOITOI, yaku.HONITSU]) <= r:
            # カウントしない
            continue

    # 小三元がある場合は、三元牌の2つが役牌になっている
    if frozenset([yaku.SHOSANGEN]) <= r:
        if not frozenset([yaku.HAKU, yaku.HATSU]) <= r and not frozenset([yaku.HATSU, yaku.CHUN]) <= r and not frozenset([yaku.CHUN, yaku.HAKU]) <= r:
            # カウントしない
            continue

    # 混老頭がある場合は、対々和になっている
    if frozenset([yaku.HONRO]) <= r:
        if yaku.TOITOI not in r:
            # カウントしない
            continue

    lastResult.add(r)

for p in lastResult:
    for y in p:
        print(yaku.YAKUINFO[y]["name"] + ",", end="")
    print()

print(len(lastResult))
