from msilib.schema import Billboard
from typing import List

class GFPolynomial:

    modulo = 0x11b

    def __init__(self, cofficient: int):
        overBitCount = cofficient.bit_length() - self.modulo.bit_length()

        cofficientShift = cofficient.bit_length() - 1
        
        while overBitCount >= 0:
            if cofficient >> cofficientShift & 1 == 1:
                cofficient ^= self.modulo << overBitCount
            overBitCount -= 1
            cofficientShift -= 1
        
        self.cofficient = cofficient
        assert(cofficient.bit_length() < self.modulo.bit_length())
        
    def __add__(self, rhs):
        return GFPolynomial(self.cofficient ^ rhs.cofficient)
    
    def __mul__(self, rhs):
        m = 0

        for i in range(self.cofficient.bit_length()):
            for j in range(rhs.cofficient.bit_length()):
                if (self.cofficient >> i & 1 == 1) and (rhs.cofficient >> j & 1 == 1):
                    m ^= (1 << (i + j))

        return GFPolynomial(m) 
    
    def pprint(self) -> str:
        poly = []
        for i in range(self.cofficient.bit_length() - 1, -1, -1):
            if self.cofficient >> i & 1 == 1:
                poly.append("x ^ " + str(i))
            
        return " + ".join(poly)
    
    def getCofficient(self):
        return self.cofficient


__inverse: List[GFPolynomial] = [GFPolynomial(0)] * 256
for i in range(256):
    for j in range(256):
        m = GFPolynomial(i) * GFPolynomial(j)
        if m.getCofficient() == 1:
            __inverse[i]= GFPolynomial(j)
            break


print(list(map(lambda x: x.getCofficient(), __inverse)))

def inverse(poly) -> GFPolynomial:
    return __inverse[poly.getCofficient()]


if __name__ == "__main__":
    a = GFPolynomial(0b11011)
    b = GFPolynomial(0b10111)
    c = a + b
    d = a * b

    assert(c.cofficient == 0b1100)
    assert(d.cofficient == 0b11101010)

    r = inverse(a)
    assert(r.cofficient == 0b11001100)

    e = r * a
    assert(e.cofficient == 1)

