from re import A, sub
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

    match len(key) * 8:
        case 128:
            Nk = 4
            Nb = 4
            Nr = 10
        case 192:
            Nk = 6
            Nb = 4
            Nr = 12
        case 256:
            Nk = 8
            Nb = 4
            Nr = 14
        case _:
            raise Exception("Key length is wrong.")

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
        
        elif Nk > 6 and count % Nk == 4:
            tmp = subWord(tmp)
        
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
    
    key = [0x8e, 0x73, 0xb0, 0xf7, 0xda, 0x0e, 0x64, 0x52, 0xc8, 0x10, 0xf3, 0x2b, 0x80, 0x90, 0x79, 0xe5, 0x62, 0xf8, 0xea, 0xd2, 0x52, 0x2c, 0x6b, 0x7b]
    w = expandKey(key)
    assert(w[51][0] == 0x01)
    assert(w[51][1] == 0x00)
    assert(w[51][2] == 0x22)
    assert(w[51][3] == 0x02)


    key = [0x60, 0x3d, 0xeb, 0x10, 0x15, 0xca, 0x71, 0xbe, 0x2b, 0x73, 0xae, 0xf0, 0x85, 0x7d, 0x77, 0x81, 0x1f, 0x35, 0x2c, 0x07, 0x3b, 0x61, 0x08, 0xd7, 0x2d, 0x98, 0x10, 0xa3, 0x09, 0x14, 0xdf, 0xf4]
    w = expandKey(key)
    assert(w[59][0] == 0x70)
    assert(w[59][1] == 0x6c)
    assert(w[59][2] == 0x63)
    assert(w[59][3] == 0x1e)
