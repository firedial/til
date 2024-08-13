from fractions import Fraction
from math import factorial

def getNextCofficients(cofficients: list[Fraction]) -> list[Fraction]:
    m = len(cofficients)
    return list(map(
        lambda right, left, index: (left + Fraction(index, 1) * right) / Fraction(m + index, 1),
        cofficients + [Fraction(0, 1)],
        [Fraction(0, 1)] + cofficients,
        range(m + 1),
    ))

def getCofficients(m: int) -> list[Fraction]:
    cofficients = [Fraction(1, 1)]
    for _ in range(m):
        cofficients = getNextCofficients(cofficients)
    return cofficients

def getProb(n: int, m: int, cofficientsList: list[list[Fraction]]) -> Fraction:
    # cofficients = getCofficients(m)
    cofficients = cofficientsList[m]

    v = Fraction(1, 1)
    prob = Fraction(0, 1)
    for k in range(m + 1):
        prob += cofficients[k] * v
        v *= Fraction(n - k)

    return prob * Fraction(factorial(n + m), pow(n, n + m))

def getTriangle(m: int) -> list[list[Fraction]]:
    cofficientsList = [[Fraction(1, 1)]]

    for _ in range(m):
        cofficientsList.append(getNextCofficients(cofficientsList[-1]))

    return cofficientsList

n = 100
m = 300
cofficientsList = getTriangle(m)
for i in range(m):
    result = getProb(n, i, cofficientsList)
    print(n + i, result, float(result))
