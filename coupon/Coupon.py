from fractions import Fraction
from math import factorial
import sys


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

    def getProbabilityList(self, maxProb: Fraction) -> list[Fraction]:
        # 最初の係数 [1, 0, 0, ..., 0] を作成
        cofficients = [Fraction(0, 1) for _ in range(self.n + 1)]
        cofficients[0] = Fraction(1, 1)

        # n に関する降べき乗 [1, n, n(n-1), ..., n!] を作成
        variables = []
        v = Fraction(1, 1)
        for i in range(self.n + 1):
            variables.append(v)
            v *= Fraction(self.n - i)

        # 最初の先頭の係数を計算
        a = Fraction(factorial(self.n), pow(self.n, self.n))

        probs = []
        i = 0
        while(True):
            # 係数と降べき乗とで内積をとる
            prob = Fraction(0, 1)
            for x, y in zip(cofficients, variables):
                prob += x * y

            # 先頭の係数をかけて結果を格納
            probs.append(a * prob)

            # 指定した確率まで計算できたらループを抜ける
            if a * prob > maxProb:
                return probs

            # 次のループの準備
            i += 1
            cofficients = self.getNextCofficients(i, cofficients)
            a *= Fraction(self.n + i, self.n)


n = int(sys.argv[1])
p = Fraction(int(sys.argv[2]), int(sys.argv[3]))

coupon = Coupon(n)
result = coupon.getProbabilityList(p)
for i, r in enumerate(result):
    print(n + i, float(r))
