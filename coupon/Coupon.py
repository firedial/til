from fractions import Fraction
from math import factorial
import functools


class Coupon():
    triangle: list[list[Fraction]] = [[Fraction(1, 1)]]

    def __init__(self, n: int):
        if n <= 0:
            raise Exception()

        self.n = n

    @functools.cache
    def getVariables(self) -> list[Fraction]:
        variables = []
        v = Fraction(1, 1)
        for i in range(self.n + 1):
            variables.append(v)
            v *= Fraction(self.n - i)

        return variables

    @functools.cache
    def getCofficient(self, r: int) -> Fraction:
        if r == self.n:
            return Fraction(factorial(self.n), pow(self.n, self.n))

        return Fraction(r, self.n) * self.getCofficient(r - 1)

    def getRow(self, m: int) -> list[Fraction]:
        calculatedRow = len(Coupon.triangle) - 1

        # 既に計算済みの場合
        if calculatedRow >= m:
            return Coupon.triangle[m]

        # 未計算の時は計算する
        for i in range(calculatedRow + 1, m + 1):
            Coupon.triangle.append(
                list(map(
                    lambda before, same, index: (before + Fraction(index, 1) * same) / Fraction(i + index, 1),
                    [Fraction(0, 1)] + Coupon.triangle[i - 1],
                    Coupon.triangle[i - 1] + [Fraction(0, 1)],
                    range(i + 1),
                ))
            )

        return Coupon.triangle[m]

    def getCoreProbability(self, r: int) -> Fraction:
        core = Fraction(0, 1)
        for x, y in zip(self.getRow(r - self.n), self.getVariables()):
            core += x * y

        return core

    def getProbabilityListUntilCount(self, r: int) -> list[Fraction]:
        # 全種類に満たないときは空配列を返す
        if self.n > r:
            return []

        a = Fraction(factorial(self.n), pow(self.n, self.n))
        probs = []

        for i in range(self.n, r + 1):
            probs.append(a * self.getCoreProbability(i))
            a *= Fraction(i + 1, self.n)

        return probs

    def getProbabilityListUntilProb(self, p: Fraction) -> list[Fraction]:
        # 1以上指定されたときは空配列を返す
        if p >= Fraction(1, 1):
            return []

        a = Fraction(factorial(self.n), pow(self.n, self.n))
        i = self.n
        probs = []

        while(True):
            probs.append(a * self.getCoreProbability(i))

            i += 1
            a *= Fraction(i, self.n)

            # 指定された確率以上であれば抜ける
            if probs[-1] >= p:
                break

        return probs


t = Coupon(120)

probs = t.getProbabilityListUntilProb(Fraction(5, 8))
for prob in probs:
    print(float(prob))