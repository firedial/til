from re import sub
from typing import List
import GFPolynomial
import sbox

def rotWord(w: List[int]) -> List[int]:
    result = [0] * 4
    for i in range(4):
        result[i] = w[(i + 1) % 4]
    
    return result

def subWord(w: List[int]) -> List[int]:
    return list(map(lambda x: sbox.sbox(x), w))


def expandKey(key: List[int]):

    Nk = 4
    Nb = 4
    Nr = 10

    rcon = 1
    w = []
    count = 0
    for i in range(Nk):
        w.append(key[i*4:(i+1)*4])
        count += 1

    
    while count < Nb * (Nr + 1):
        tmp = w[count - 1]
        if (count % Nk == 0):
            tmp = subWord(rotWord(tmp))
            tmp[0] ^= GFPolynomial.GFPolynomial(rcon).cofficient
            
            rcon = rcon + rcon
        
        w.append(list(map(lambda x, y: x ^ y, w[count - Nk], tmp)))
        count += 1
    
    return w


if __name__ == "__main__":
    key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
    w = expandKey(key)
    assert(w[43][0] == 0xb6)
    assert(w[43][1] == 0x63)
    assert(w[43][2] == 0x0c)
    assert(w[43][3] == 0xa6)

    





