import unittest
from util.hand import wait


class waitTest(unittest.TestCase):
    def test_wait(self):
        """
        和了牌のリスト取得
        """
        self.assertEqual(wait.getWaitingHai([1]), [True])
        self.assertEqual(wait.getWaitingHai([3, 1, 1, 1, 1, 1, 1, 1, 3]), [True, True, True, True, True, True, True, True, True])
        self.assertEqual(wait.getWaitingHai([0, 4, 4, 2, 0, 0, 0, 0, 0]), [True, False, False, True, True, False, False, False, False])

    def test_count(self):
        """
        和了牌の種類数
        """
        self.assertEqual(wait.countWaitingHai([1]), 1)
        self.assertEqual(wait.countWaitingHai([1, 1, 1, 1, 1, 1, 1]), 3)
        self.assertEqual(wait.countWaitingHai([3, 1, 1, 1, 1, 1, 1, 1, 3]), 9)
