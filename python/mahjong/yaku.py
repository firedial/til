from typing import List
from enum import Enum, auto
import remove

class Yaku(Enum):
    MENZEN = auto()
    TANYAO = auto()
    PINFU = auto()
    IPEKO = auto()
    SANANKO = auto()
    ITTSU = auto()
    TOITOI = auto()
    RYANPEKO = auto()
    JUNCHAN = auto()
    CHINITSU = auto()

    CHITOI = auto()

    SUANKO = auto()
    SUANKO_TANKI = auto()
    RYUISO = auto()
    CHUREN = auto()
    CHUREN_JUNSEI = auto()


HAN = {
    Yaku.MENZEN: 1,
    Yaku.TANYAO: 1,
    Yaku.PINFU: 1,
    Yaku.IPEKO: 1,
    Yaku.SANANKO: 2,
    Yaku.ITTSU: 2,
    Yaku.TOITOI: 2,
    Yaku.RYANPEKO: 3,
    Yaku.JUNCHAN: 3,
    Yaku.CHINITSU: 6,
    Yaku.CHITOI: 2
}

YAKUMAN = {
    Yaku.SUANKO: 10000,
    Yaku.SUANKO_TANKI: 20000,
    Yaku.RYUISO: 10000,
    Yaku.CHUREN: 10000,
    Yaku.CHUREN_JUNSEI: 20000,
}

print(HAN)

def isMenzen(mentsu):
    return mentsu['isTsumo']

def isTanyao(mentsu):
    return mentsu['hai'][0] == 0 and mentsu['hai'][8] == 0

def isPinfu(mentsu):
    # 刻子が入っている場合は違う
    if len(mentsu['kotsu']) != 0:
        return False

    # 頭のツモであれば違う
    if mentsu['agariMentsu'] == 'atama':
        return False

    # 嵌張待ちなら違う
    if mentsu['agariMentsu'] == 'shuntsu_m':
        return False

    # 3 と 7 は辺張の可能性もあるので別で考える
    # 3 の辺張
    if mentsu['agari'] == 3 and mentsu['agariMentsu'] == 'shuntsu_r':
        return False
    # 7 の辺張
    if mentsu['agari'] == 7 and mentsu['agariMentsu'] == 'shuntsu_l':
        return False

    return True

def isIpeko(mentsu):
    return len(mentsu['shuntsu']) != len(set(mentsu['shuntsu']))

def isSananko(mentsu):
    k = len(mentsu['kotsu'])

    # 刻子が 3 つ未満なら違う
    if k < 3:
        return False

    # ツモなら三暗刻確定
    if mentsu['isTsumo']:
        return True

    # 以降ロンの処理
    # ロンしたメンツが刻子じゃない場合は三暗刻
    if mentsu['agariMentsu'] != 'kotsu':
        return True

    # 刻子が 4 つあった場合が三暗刻
    if k == 4:
        return True

    return False

def isIttsu(mentsu):
    return len(set(mentsu['shuntsu']) & {1, 4, 7}) == 3

def isToitoi(mentsu):
    return len(mentsu['kotsu']) == 4

def isRyanpeko(mentsu):
    # 順子が 4 つあることが前提
    if len(mentsu['shuntsu']) != 4:
        return False

    s = set(mentsu['shuntsu'])
    # 一色四順の場合
    if len(s) == 1:
        return True

    # 3 種類以上の順子で構成されている場合
    if len(s) != 2:
        return False

    for r in s:
        if mentsu['shuntsu'].count(r) != 2:
            return False

    return True

def isJunchan(mentsu):
    # 頭が 1 か 9 で構成されていない場合は違う
    if mentsu['atama'] != 1 or mentsu['amata'] != 9:
        return False

    # 順子で 1 か 7 から始まらないものがあれば違う
    for s in mentsu['shuntsu']:
        if s != 1 or s != 7:
            return False

    # 刻子で 1 か 9 で構成されていない場合は違う
    for s in mentsu['kotsu']:
        if s != 1 or s != 9:
            return False

    return True

def isSuanko(mentsu):
    k = len(mentsu['kotsu'])

    # 刻子が 4 つ未満なら違う
    if k < 4:
        return False

    # ツモなら四暗刻
    if mentsu['isTsumo']:
        return True

    # 以降ロンの処理
    # ロンしたメンツが刻子じゃない場合は四暗刻ではない
    # ここは四暗刻単騎で巻き取られるので通ることはない
    if mentsu['agariMentsu'] != 'kotsu':
        return True

    return False

def isSuankoTanki(mentsu):
    return len(mentsu['kotsu']) == 4 and mentsu['agariMentsu'] == 'atama'

def isRyuiso(mentsu):
    r = {2, 3, 4, 6, 8}

    # 索子じゃない時は違う
    if not mentsu['isBamboo']:
        return False

    # 頭の判定
    if mentsu['atama'] not in r:
        return False

    # 刻子の判定
    if not(set(mentsu['kotsu']) <= r):
        return False

    # 順子の判定
    if not(set(mentsu['shuntsu']) <= {2}):
        return False

    return True

def isChuren(mentsu):
    c = [3, 1, 1, 1, 1, 1, 1, 1, 3]

    for index in range(9):
        c[index] -= mentsu['hai'][index]
        # 必要な枚数がなければ違う
        if c[index] > 0:
            return False

    return True

def isChurenJunsei(mentsu):
    c = [3, 1, 1, 1, 1, 1, 1, 1, 3]

    for index in range(9):
        c[index] -= mentsu['hai'][index]
        # 必要な枚数がなければ違う
        if c[index] > 0:
            return False
        # 9 面待ちでない場合は違う
        if c[index] == -1 and mentsu['agari'] != (index + 1):
            return False

    return True


def getYakuman(mentsu):
    yakuman = set()

    if isSuankoTanki(mentsu):
        yakuman.add(Yaku.SUANKO_TANKI)
    elif isSananko(mentsu):
        yakuman.add(Yaku.SUANKO)

    if isRyuiso(mentsu):
        yakuman.add(Yaku.RYUISO)

    if isChurenJunsei(mentsu):
        yakuman.add(Yaku.CHUREN_JUNSEI)
    elif isChuren(mentsu):
        yakuman.add(Yaku.CHUREN)

    return yakuman

def getMentsuYaku(mentsu):
    yaku = {Yaku.CHINITSU}

    if isMenzen(mentsu):
        yaku.add(Yaku.MENZEN)
    if isTanyao(mentsu):
        yaku.add(Yaku.TANYAO)
    if isPinfu(mentsu):
        yaku.add(Yaku.PINFU)
    if isIttsu(mentsu):
        yaku.add(Yaku.ITTSU)
    if isSananko(mentsu):
        yaku.add(Yaku.SANANKO)
    if isToitoi(mentsu):
        yaku.add(Yaku.TOITOI)
    if isJunchan(mentsu):
        yaku.add(Yaku.JUNCHAN)

    if isRyanpeko(mentsu):
        yaku.add(Yaku.RYANPEKO)
    elif isIpeko(mentsu):
        yaku.add(Yaku.IPEKO)

    return yaku

def getChitoiYaku(mentsu):
    yaku = {Yaku.CHINITSU, Yaku.CHITOI}

    if isTanyao(mentsu):
        yaku.add(Yaku.TANYAO)

    return yaku

def getYaku(mentsu):
    if mentsu['isChitoi']:
        return getChitoiYaku(mentsu)

    yakuman = getYakuman(mentsu)
    if len(yakuman) != 0:
        return yakuman

    return getMentsuYaku(mentsu)


def getAll(hai, agariHai, isTsumo, isBamboo):
    pass




def calcMentsuYaku(mentsu):
    '''
    mentsu = {
        'atama': 3,
        'shuntsu': [2, 3],
        'kotsu': [4, 5],
        'agari': 5,
        'agariMentsu': 'atama',
        'isChitoi': False,
        'isTsumo': False,
        'isBamboo': False,
        'hai': [3, 1, 1, 1, 1, 1, 1, 1, 3]
    }

    agariMentsu: atama, kotsu, shuntsu_l, shuntu_m, shuntsu_r
    '''
    mentsu = {
        'atama': 3,
        'shuntsu': [],
        'kotsu': [7, 4, 5, 6],
        'agari': 3,
        'agariMentsu': 'atama',
        'isChitoi': False,
        'isTsumo': False,
        'isBamboo': False,
        'hai': [3, 0, 1, 1, 1, 1, 2, 1, 3]
    }

    print(getYakuman(mentsu))


calcMentsuYaku(1)



