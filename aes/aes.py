
from typing import List
import sbox
import mixColumnsMul
import ExpandKey



def subBytes(state):
    return list(map(lambda x: sbox.sbox(x), state))

def shiftRows(state):
    result = [0] * 16
    for i in range(16):
        result[i] = state[(i + (i % 4) * 4) % 16]
    
    return result
 

def mixColumns(state):
    a = [0x02, 0x01, 0x01, 0x03]
    
    result = []
    for i in range(4):
        result.extend(mixColumnsMul.mixColumn(a, state[i*4:(i+1)*4]))
    
    return result


def addRoundKey(state, w):
    result = [0] * 16
    for i in range(16):
        result[i] = state[i] ^ w[i // 4][i % 4]

    return result



def cipher(plain: List[int], key: List[int]):

    Nb = 4
    Nk = 4
    Nr = 10

    assert(len(plain) == 16)
    assert(len(key) == 16)

    expandedKey = ExpandKey.expandKey(key)

    state = plain

    state = addRoundKey(state, expandedKey[0:Nb])

    for i in range(1, Nr):
        state = subBytes(state)
        state = shiftRows(state)
        state = mixColumns(state)
        state = addRoundKey(state, expandedKey[i*Nb:(i+1)*Nb])
        
    state = subBytes(state)
    state = shiftRows(state)
    state = addRoundKey(state, expandedKey[Nr*Nb:(Nr+1)*Nb])

    return state
        
plain = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
c = cipher(plain, key)
print(list(map(lambda x: hex(x), c)))

# state = [0x19, 0x3d, 0xe3, 0xbe, 0xa0, 0xf4, 0xe2, 0x2b, 0x9a, 0xc6, 0x8d, 0x2a, 0xe9, 0xf8, 0x48, 0x08]
# print(list(map(lambda x: hex(x), state)))
# state = list(map(lambda x: sbox.sbox(x), state))
# print(list(map(lambda x: hex(x), state)))
# state = shiftRows(state)
# print(list(map(lambda x: hex(x), state)))
# state = mixColumns(state)
# print(list(map(lambda x: hex(x), state)))





