
def nextHai(hai):
    if hai[0] != 0:
        return nextHaiNonZeroFirst(hai)
    else:
        return nextHaiZeroFirst(hai)


def nextHaiNonZeroFirst(hai):
    haiLen = len(hai)
    index = 1
    first = hai[0]
    hai[0] = 0
    while index < haiLen:
        if hai[index] != 0:
            hai[index - 1] = first + 1
            hai[index] -= 1
            return hai
        index += 1

    hai[haiLen - 1] = first
    return hai

def nextHaiZeroFirst(hai):
    haiLen = len(hai)
    index = 0
    while index < haiLen:
        if hai[index] != 0:
            hai[index - 1] += 1
            hai[index] -= 1
            return hai
        index += 1
    

