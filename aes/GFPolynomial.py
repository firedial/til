
class GFPolynomial:

    modulo = 0x11b

    def __init__(self, cofficient: int):
        self.cofficient = cofficient

    def __add__(self, rhs):
        return GFPolynomial(self.cofficient ^ rhs.cofficient)
    
    def __mul__(self, rhs):
        r = 0
        lhs = self.cofficient
        
        while True:
            if lhs == 0:
                break

            r <<= 1
            if r.bit_length() == self.modulo.bit_length():
                r ^= self.modulo

            if lhs & 1 == 1:
                r ^= rhs.cofficient
            
            lhs >>= 1
        return GFPolynomial(r)

    
    def pprint(self) -> str:
        poly = []
        for i in range(self.cofficient.bit_length() - 1, -1, -1):
            if self.cofficient >> i & 1 == 1:
                poly.append("x ^ " + str(i))
            
        return " + ".join(poly)
    
    def getCofficient(self):
        return self.cofficient



if __name__ == "__main__":
    a = GFPolynomial(0b11011)
    b = GFPolynomial(0b10111)
    c = a + b
    d = a * b
    assert(c.getCofficient() == 0b1100)
    assert(d.getCofficient() == 0b11101010)

    print(a.pprint())
    print(b.pprint())
    print(c.pprint())
    print(d.pprint())
