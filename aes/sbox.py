
import GFPolynomial as gfpoly

def sbox(b: int) -> int:
    c = [1, 1, 0, 0, 0, 1, 1, 0]
    inverse =  gfpoly.inverse(gfpoly.GFPolynomial(b))

    inverseBit = []
    for i in range(8):
        inverseBit.append(inverse.cofficient >> i & 1)

    resultBit = []
    for i in range(8):
        resultBit.append(
            inverseBit[i] ^
            inverseBit[(i + 4) % 8] ^
            inverseBit[(i + 5) % 8] ^
            inverseBit[(i + 6) % 8] ^
            inverseBit[(i + 7) % 8] ^
            c[i]
            )
    
    result = 0
    for i in range(8):
        result ^= resultBit[i] << i

    return result

if __name__ == "__main__":
    assert(sbox(0x7f) == 0xd2)
    assert(sbox(0x91) == 0x81)
    assert(sbox(0x00) == 0x63)
    assert(sbox(0x52) == 0x00)

    





    








