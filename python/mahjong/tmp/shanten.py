import agari

def getAgariHai(hai):
    haiLen = len(hai)
    agariHai = []

    index = 0
    while index < haiLen:
        if hai[index] == 4:
            agariHai.append(False)
            index += 1
            continue

        hai[index] += 1
        agariHai.append(agari.isAgari(hai))
        hai[index] -= 1

        index += 1
    
    return agariHai
    
def isTempai(hai):
    return len(list(filter(lambda x: x, getAgariHai(hai)))) > 0
    


    

