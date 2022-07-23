
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



def cipher(plainString: str, keyString: str):
    plain = [int(("0x" + plainString[i:i+2]), 16) for i in range(0, len(plainString), 2)]
    key = [int(("0x" + keyString[i:i+2]), 16) for i in range(0, len(keyString), 2)]

    assert(len(plain) == 16)

    match len(key) * 8:
        case 128:
            Nb = 4
            Nr = 10
        case 192:
            Nb = 4
            Nr = 12
        case 256:
            Nb = 4
            Nr = 14
        case _:
            raise Exception("Key length is wrong.")

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

    return "".join(list(map(lambda x: '{:02x}'.format(x), state)))
        
if __name__ == "__main__":
    plain = "00112233445566778899aabbccddeeff"
    key = "000102030405060708090a0b0c0d0e0f"
    c = cipher(plain, key)
    assert(c == "69c4e0d86a7b0430d8cdb78070b4c55a")


    plain = "00112233445566778899aabbccddeeff"
    key = "000102030405060708090a0b0c0d0e0f1011121314151617"
    c = cipher(plain, key)
    assert(c == "dda97ca4864cdfe06eaf70a0ec0d7191")

    plain = "00112233445566778899aabbccddeeff"
    key = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"
    c = cipher(plain, key)
    assert(c == "8ea2b7ca516745bfeafc49904b496089")

