import unittest
from util.hand import agari


class agariTest(unittest.TestCase):
    def test_agari(self):
        """
        通常パターンの和了テスト
        """
        self.assertTrue(agari.isAgari([]))
        self.assertFalse(agari.isAgari([1]))
        self.assertTrue(agari.isAgari([2]))
        self.assertTrue(agari.isAgari([3]))
        self.assertFalse(agari.isAgari([4]))

        self.assertTrue(agari.isAgari([2, 3, 3]))
        self.assertTrue(agari.isAgari([2, 3, 1, 1, 1]))
        self.assertTrue(agari.isAgari([1, 1, 3, 1, 1, 1]))

        self.assertTrue(agari.isAgari([2, 0, 3, 0, 3]))
        self.assertTrue(agari.isAgari([2, 0, 3, 3, 3]))

    def test_churen_agari(self):
        """
        九蓮宝燈の和了のテスト
        """
        self.assertTrue(agari.isAgari([3, 1, 1, 1, 1, 1, 1, 1, 4]))
        self.assertTrue(agari.isAgari([3, 1, 1, 1, 1, 1, 1, 2, 3]))
        self.assertTrue(agari.isAgari([3, 1, 1, 1, 1, 1, 2, 1, 3]))
        self.assertTrue(agari.isAgari([3, 1, 1, 1, 1, 2, 1, 1, 3]))
        self.assertTrue(agari.isAgari([3, 1, 1, 1, 2, 1, 1, 1, 3]))
        self.assertTrue(agari.isAgari([3, 1, 1, 2, 1, 1, 1, 1, 3]))
        self.assertTrue(agari.isAgari([3, 1, 2, 1, 1, 1, 1, 1, 3]))
        self.assertTrue(agari.isAgari([3, 2, 1, 1, 1, 1, 1, 1, 3]))
        self.assertTrue(agari.isAgari([4, 1, 1, 1, 1, 1, 1, 1, 3]))

    def test_chitoi_agari(self):
        """
        七対子の和了テスト
        """
        self.assertFalse(agari.isSevenPairs([1, 1, 3, 1, 1, 1]))
        self.assertFalse(agari.isSevenPairs([2, 2, 0, 2, 0]))
        self.assertTrue(agari.isSevenPairs([2, 2, 2, 2, 2, 2, 2]))
        self.assertFalse(agari.isSevenPairs([2, 2, 2, 2, 2, 2, 2, 2]))
