import math

def getProbableRange(h, n):
    upperBound = n * (n - 1) / (2 * h)

    lowerBound1 = 1 - math.exp(-n * (n- 1) / (2 * h))
    lowerBound2 = 0
    if n * n <= 2 * h:
        lowerBound2 = 0.3 * n * (n - 1) / h

    lowerBound = lowerBound1 if lowerBound1 > lowerBound2 else lowerBound2

    return (lowerBound, upperBound)

def getMaxNumberUnderProbabilty(h, p):
    f = lambda h, p, a, b: a if b - a <= 1 else f(h, p, (a + b) // 2, b) if getProbableRange(h, (a + b) // 2)[1] < p else f(h, p, a, (a + b) // 2)
    return f(h, p, 1, h)

h = 2 ** 256
p = 10 ** -47.9

n = getMaxNumberUnderProbabilty(h, p)
print(f"{n:.3E}")

n = 3.153 * 10 ** 21

(lowerBound, upperBound) = getProbableRange(h, n)
print(f"{lowerBound} < p < {upperBound}")

print(2 ** 256)
print(6 ** 99)

