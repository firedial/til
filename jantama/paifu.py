from dataclasses import dataclass

@dataclass
class Paifu:
    paifu: dict

    def __init__(self, paifu: dict):
        self.paifu = paifu

    def allTime(self) -> int:
        return self.paifu["head"]["end_time"] - self.paifu["head"]["start_time"]

