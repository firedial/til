import unittest
from util.hand.HandUtil import HandUtil
from util.handLoop import nextHand


class HandUtilTest(unittest.TestCase):
    def test_agari(self):
        handUtil = HandUtil()

        handUtil.setHand([3, 1, 1, 1, 1, 1, 1, 1, 4])
        self.assertTrue(handUtil.isAgari())

        handUtil.setHand([3, 1, 1, 1, 1, 1, 1, 2, 3])
        self.assertTrue(handUtil.isAgari())

    def test_number(self):
        """
        牌番号が正しく払いだされて、復元可能かを見る
        """
        handUtil = HandUtil()
        handUtilSet = HandUtil()
        numbers = [1, 2, 4, 7, 8, 10, 11, 13]
        numbers = [1, 2, 4, 7]

        for num in numbers:
            hand = [0, 0, 0, 0, 0, 0, 0, 0, num]
            while True:
                handUtil.setHand(hand)
                if handUtil.isNeedIrreducible():
                    number = handUtil.getHandNumber()
                    handUtilSet.setHandByNumber(number)
                    self.assertEqual(handUtilSet.getHand(), handUtil.getHand())

                    # 雀頭接続順子も考える
                    if handUtil.hasAtamaConnectedShuntsu():
                        handUtil.setHand(hand, True)
                        number = handUtil.getHandNumber()
                        handUtilSet.setHandByNumber(number)
                        self.assertEqual(handUtilSet.getHand(), handUtil.getHand())

                hand = nextHand(hand)
                if hand == [0, 0, 0, 0, 0, 0, 0, 0, num]:
                    break


if __name__ == "__main__":
    unittest.main()
