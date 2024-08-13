from fractions import Fraction
from math import factorial

def getNextCofficients(cofficients: list[Fraction]) -> list[Fraction]:
    m = len(cofficients)
    if m == 0:
        return [Fraction(1, 1)]

    return list(map(
        lambda right, left, index: (left + Fraction(index, 1) * right) / Fraction(m + index, 1),
        cofficients + [Fraction(0, 1)],
        [Fraction(0, 1)] + cofficients,
        range(m + 1),
    ))

def getProb(n: int, p: int) -> list[Fraction]:
    if n <= 0 or n > p:
        return []

    m = p - n
    cofficients = []
    a = Fraction(factorial(n - 1), pow(n, n - 1))
    probs = []

    for i in range(m + 1):
        cofficients = getNextCofficients(cofficients)
        a *= Fraction(n + i, n)

        v = Fraction(1, 1)
        prob = Fraction(0, 1)
        for k in range(i + 1):
            prob += cofficients[k] * v
            v *= Fraction(n - k)

        probs.append(a * prob)
        print(n + i, a * prob, float(a * prob))

    return probs

n = 48
p = 500

getProb(n, p)
