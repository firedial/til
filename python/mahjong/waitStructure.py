import agari

MAX_HAI_NUMBER = 4

def getWaitingStructure(hai):
    haiLen = len(hai)
    waitingStructure = []

    # 各牌に対して一枚減らして和了かどうか確認していく
    for index in range(0, haiLen):
        # 存在する牌の枚数以上持っていた場合は和了牌とならない

        hai_ = hai[:]
        if hai_[index] >= MAX_HAI_NUMBER:
            waitingStructure.append([
                False, False, False, False
            ])
            continue


        # 単騎
        hai_ = hai[:]
        hai_[index] -= 1
        tanki = agari.isAgari(hai_)

        # シャンポン
        hai_ = hai[:]
        hai_[index] -= 2
        shanpon = agari.isAgari(hai_)

        # カンチャン
        if (index == 0 or index == haiLen - 1):
            kanchan = False
        else:
            hai_ = hai[:]
            hai_[index - 1] -= 1
            hai_[index + 1] -= 1
            kanchan = agari.isAgari(hai_)

        # リャンメン
        if (haiLen <= 3):
            ryanmenA = False
            ryanmenB = False
        elif (index >= haiLen - 3):
            hai_ = hai[:]
            hai_[index - 1] -= 1
            hai_[index - 2] -= 1
            ryanmenA = agari.isAgari(hai_)
            ryanmenB = False
        elif (index <= 2):
            hai_ = hai[:]
            hai_[index + 1] -= 1
            hai_[index + 2] -= 1
            ryanmenA = False
            ryanmenB = agari.isAgari(hai_)
        else:
            hai_ = hai[:]
            hai_[index - 1] -= 1
            hai_[index - 2] -= 1
            ryanmenA = agari.isAgari(hai_)

            hai_ = hai[:]
            hai_[index + 1] -= 1
            hai_[index + 2] -= 1
            ryanmenB = agari.isAgari(hai_)

        ryanmen = ryanmenA or ryanmenB

        # waitingStructure.append({
        #     'tanki': tanki,
        #     'shanpon': shanpon,
        #     'kanchan': kanchan,
        #     'ryanmen': ryanmen
        # })


        waitingStructure.append([
            tanki, shanpon, kanchan, ryanmen
        ])

    return waitingStructure

def countWaitingStructure(hai):
    return sum(map(lambda x: len(list(filter(lambda y: y, x))) , getWaitingStructure(hai)))

if __name__ == '__main__':
    print(getWaitingStructure([1, 3, 1]))
    print(countWaitingStructure([1, 3, 1]))
    print(countWaitingStructure([3, 1, 1, 1, 1, 1, 1, 1, 3]))
