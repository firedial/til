import agari

MAX_HAI_NUMBER = 4

def getWaitingHai(hai):
    haiLen = len(hai)
    waitingHai = []

    # 各牌に対して一枚ずつ増やして和了かどうか確認していく
    for index in range(0, haiLen):
        # 存在する牌の枚数以上持っていた場合は和了牌とならない
        if hai[index] >= MAX_HAI_NUMBER:
            waitingHai.append(False)

        hai_ = hai[:]
        hai_[index] += 1
        waitingHai.append(agari.isAgari(hai_))

    return waitingHai

def countWaitingHai(hai):
    return len(list(filter(lambda x: x, getWaitingHai(hai))))
    
    
if __name__ == '__main__':
    print(getWaitingHai([3, 1, 1, 1, 1, 1, 1, 1, 3]))
    print(countWaitingHai([1, 1, 1, 1, 1, 1, 1]))
    print(countWaitingHai([3, 1, 1, 1, 1, 1, 1, 1, 3]))


