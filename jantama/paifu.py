from dataclasses import dataclass
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

@dataclass
class Tile:
    tiles: list[str]

    def __init__(self, tiles: dict):
        self.tiles = tiles

    def action(self, action: dict):
        pass

    def getShanten(self) -> int:
        m = "".join(list(map(lambda x: x[0], (filter(lambda x: x[-1] == "m", self.tiles)))))
        p = "".join(list(map(lambda x: x[0], (filter(lambda x: x[-1] == "p", self.tiles)))))
        s = "".join(list(map(lambda x: x[0], (filter(lambda x: x[-1] == "s", self.tiles)))))
        h = "".join(list(map(lambda x: x[0], (filter(lambda x: x[-1] == "z", self.tiles)))))
        shanten = Shanten()
        tiles = TilesConverter.string_to_34_array(man=m, pin=p, sou=s, honors=h)

        return shanten.calculate_shanten(tiles)

@dataclass
class Round:
    tiles0: Tile
    tiles1: Tile
    tiles2: Tile
    tiles3: Tile

    def __init__(self, action: dict):
        self.tiles0 = Tile(action["result"]["data"]["tiles0"])
        self.tiles1 = Tile(action["result"]["data"]["tiles1"])
        self.tiles2 = Tile(action["result"]["data"]["tiles2"])
        self.tiles3 = Tile(action["result"]["data"]["tiles3"])

        print(self.tiles0.getShanten())

    def execute(self, action: dict):
        return
        # 牌譜のタイプが1の時に記録されている(そして result のキーを持つ)
        if action["type"] != 1:
            return False

        match action["result"]["name"]:
            case ".lq.RecordDealTile": # 自摸
                pass
            case ".lq.RecordDiscardTile": # 打牌
                pass
            case ".lq.RecordChiPengGang": # チー、ポン、大明槓
                pass
            case ".lq.RecordAnGangAddGang": # 暗槓、加槓
                pass

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

    def debug(self) -> str:
        actions = self.paifu["data"]["data"]["actions"]
        for action in actions:
            if self.isNewRound(action):
                round = Round(action)
            else:
                pass
                # round.execute(action)
