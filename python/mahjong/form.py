
# 4 枚以上使っていないかをみる
def isOverFour(hai):
    return len(list(filter(lambda x: x > 4, hai))) > 0

# 標準形かどうかをみる(先頭が 0 でなく前方重心)
def isNormalForm(hai):
    if hai[0] == 0:
        return False

    return isFormerGravity(hai)
    

def isFormerGravity(hai):
    haiLen = len(hai)
    first = 0
    last = haiLen - 1

    while first < haiLen:
        if hai[first] != 0:
            break
        first += 1

    while 0 <= last:
        if hai[last] != 0:
            break
        last -= 1

    while first < last:
        if hai[first] > hai[last]:
            return True
        if hai[first] < hai[last]:
            return False
        first += 1
        last -= 1

    return True
