from fractions import Fraction
import sys

class SeironIsNotGoodForPeople():
    def __init__(self, n: int):
        if n <= 0:
            raise Exception("n is wrong")

        self.n = n

    def getNextProbs(self, probs: list[Fraction]) -> list[Fraction]:
        return list(map(
            lambda same, diff, index: ((self.n - Fraction(index, 1) + Fraction(1, 1)) * diff + Fraction(index, 1) * same) / Fraction(self.n, 1),
            probs,
            [Fraction(0, 1)] + probs[:-1],
            range(len(probs)),
        ))

    def getProbabilityList(self, maxProb: Fraction) -> None:
        if maxProb >= Fraction(1, 1):
            raise Exception("p is wrong")

        # 最初の確率 [1, 0, 0, ..., 0] を作成
        probs = [Fraction(0, 1) for _ in range(self.n + 1)]
        probs[0] = Fraction(1, 1)

        i = 0
        while(True):
            # 結果を出力
            print(i, list(map(lambda x: format(float(x), '.3g'), probs)))

            # 指定した確率まで計算できたらループを抜ける
            if probs[-1] > maxProb:
                break

            # 次のループの準備
            i += 1
            probs = self.getNextProbs(probs)



n = int(sys.argv[1])
p = Fraction(int(sys.argv[2]), int(sys.argv[3]))

coupon = SeironIsNotGoodForPeople(n)
result = coupon.getProbabilityList(p)
