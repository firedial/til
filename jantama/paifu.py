from dataclasses import dataclass

@dataclass
class Paifu:
    paifu: dict

    def __init__(self, paifu: dict):
        self.paifu = paifu

    def allTime(self) -> int:
        return self.paifu["head"]["end_time"] - self.paifu["head"]["start_time"]

    @staticmethod
    def isFinishedRound(action: dict) -> bool:
        # 牌譜のタイプが1の時に記録されている(そして result のキーを持つ)
        if action["type"] != 1:
            return False

        # 荒牌平局
        if action["result"]["name"] == ".lq.RecordNoTile":
            return True

        # 途中流局
        if action["result"]["name"] == ".lq.RecordLiuJu":
            return True

        # 和了
        if action["result"]["name"] == ".lq.RecordHule":
            return True

        return False

    @staticmethod
    def isNewRound(action: dict) -> bool:
        return action["type"] == 1 and action["result"]["name"] == ".lq.RecordNewRound"

