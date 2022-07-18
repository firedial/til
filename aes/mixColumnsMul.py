
from typing import List
import GFPolynomial

def mixColumn(a: List[int], b: List[int]):
    mul = [GFPolynomial.GFPolynomial(0)] * 4

    for i in range(4):
        for j in range(4):
            mul[(i + j) % 4] += GFPolynomial.GFPolynomial(a[i]) * GFPolynomial.GFPolynomial(b[j])

    return list(map(lambda x: x.cofficient, mul))

if __name__ == "__main__":
    a = [0x02, 0x01, 0x01, 0x03]
    b = [0x0e, 0x09, 0x0d, 0x0b]

    print(mixColumn(a, b))



