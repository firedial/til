
def getNonZeroHai(pattern):
    isNonZero = lambda hai: len(list(filter(lambda x: x < 0, hai))) == 0
    return list(filter(isNonZero, pattern))

def removedAtamaPattern(hai):
    haiLen = len(hai)
    pattern = []

    for index in range(0, haiLen):
        pattern.append(hai.copy())
        pattern[index][index] -= 2

    return getNonZeroHai(pattern)

def removedKotsuPattern(hai):
    haiLen = len(hai)
    pattern = []

    for index in range(0, haiLen):
        pattern.append(hai.copy())
        pattern[index][index] -= 3

    return getNonZeroHai(pattern)

def removedShuntsuPattern(hai):
    haiLen = len(hai)
    pattern = []

    for index in range(0, haiLen - 2):
        pattern.append(hai.copy())
        pattern[index][index] -= 1 
        pattern[index][index + 1] -= 1 
        pattern[index][index + 2] -= 1 

    return getNonZeroHai(pattern)

def removedAtamaConnectedShuntsuPattern(hai):
    haiLen = len(hai)
    patternAsc = []
    patternDesc = []

    for index in range(0, haiLen - 2):
        patternAsc.append(hai.copy())
        patternAsc[index][index] -= 3 
        patternAsc[index][index + 1] -= 1 
        patternAsc[index][index + 2] -= 1 

        patternDesc.append(hai.copy())
        patternDesc[index][index] -= 1
        patternDesc[index][index + 1] -= 1 
        patternDesc[index][index + 2] -= 3

    return getNonZeroHai(patternAsc + patternDesc)

def removedMentsuPattern(hai):
    return removedKotsuPattern(hai) + removedShuntsuPattern(hai)

def removedSendableForm(hai):
    return removedAtamaPattern(hai) + removedAtamaConnectedShuntsuPattern(hai)


if __name__ == '__main__':
    print(removedKotsuPattern([1, 2, 3]))
    print(removedShuntsuPattern([1, 2, 3, 3, 2, 0]))
    print(removedMentsuPattern([1, 2, 3, 3, 2, 0]))
    
    print(removedAtamaConnectedShuntsuPattern([1, 2, 3, 5, 2, 3]))
    print(removedSendableForm([1, 2, 3, 5, 2, 3]))
        



