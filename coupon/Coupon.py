from fractions import Fraction
from math import factorial

class Coupon():
    def __init__(self, n: int):
        if n <= 0:
            raise Exception()

        self.n = n

    @staticmethod
    def getNextCofficients(m: int, cofficients: list[Fraction]) -> list[Fraction]:
        return list(map(
            lambda same, diff, index: (diff + Fraction(index, 1) * same) / Fraction(m + index, 1),
            cofficients,
            [Fraction(0, 1)] + cofficients[:-1],
            range(len(cofficients)),
        ))

    def getProb(self, maxProb: Fraction) -> list[Fraction]:
        cofficients = [Fraction(0, 1) for _ in range(self.n + 1)]
        cofficients[0] = Fraction(1, 1)

        variables = []
        v = Fraction(1, 1)
        for i in range(self.n + 1):
            variables.append(v)
            v *= Fraction(self.n - i)

        a = Fraction(factorial(self.n), pow(self.n, self.n))
        probs = []
        i = 0

        while(True):
            prob = Fraction(0, 1)
            for x, y in zip(cofficients, variables):
                prob += x * y
            probs.append(a * prob)

            if a * prob > maxProb:
                return probs

            i += 1
            cofficients = self.getNextCofficients(i, cofficients)
            a *= Fraction(self.n + i, self.n)


coupon = Coupon(20)
result = coupon.getProb(Fraction(1, 1) - Fraction(1, 100))
for i, r in enumerate(result):
    print(i, float(r))


