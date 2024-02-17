from dataclasses import dataclass
from typing import ClassVar
import random


@dataclass(frozen=True)
class Card:
    number: int

    def __init__(self, number: int):
        # 0 は 10 とみなす
        if number == 0:
            number = 10

        if number < 5 or number > 10:
            raise ValueError("Wrong company number.")

        object.__setattr__(self, "number", number)

    def __str__(self) -> str:
        return str(self.number % 10)

@dataclass
class Tip:
    count: int

    def __init__(self, count: int):
        object.__setattr__(self, "count", count)

    def getCount(self) -> int:
        return self.count

    def addCount(self, tip: int) -> None:
        self.count += tip

    def __add__(self, other):
        return Tip(self.count + other.count)

    def __sub__(self, other):
        return Tip(self.count - other.count)

    def __str__(self) -> str:
        return str(self.count)

@dataclass
class OpenHand:
    companies: dict[Card, tuple[int, bool]]

    def __init__(self):
        object.__setattr__(self, "companies", {
            Card(5): (0, False),
            Card(6): (0, False),
            Card(7): (0, False),
            Card(8): (0, False),
            Card(9): (0, False),
            Card(10): (0, False),
        })

    def addCard(self, card: Card) -> None:
        self.companies[card] = (self.companies[card][0] + 1, self.companies[card][1])

    def getOpenHandByCard(self, card: Card) -> tuple[int, bool]:
        return self.companies[card]

    def onMonopoly(self, card: Card) -> None:
        self.companies[card] = (self.companies[card][0], True)

    def offMonopoly(self, card: Card) -> None:
        self.companies[card] = (self.companies[card][0], False)

    def getNonMonopolyCards(self) -> list[Card]:
        return list(dict((filter(lambda company: not company[1][1], self.companies.items()))))

    def __str__(self) -> str:
        s = ""
        for card, hand in self.companies.items():
            s += ("o" if hand[1] else "x") + str(card) + str(hand[0]) + ","
        return s

@dataclass
class Player:
    closedHand: list[Card]
    openHand: OpenHand
    tip: Tip

    def __init__(self, cards: list[Card]):
        if len(cards) != 3:
            raise ValueError("Wrong cards count.")

        object.__setattr__(self, "openHand", OpenHand())
        object.__setattr__(self, "closedHand", cards)
        object.__setattr__(self, "tip", Tip(10))
        object.__setattr__(self, "drawCard", None)

    def getTip(self) -> Tip:
        return self.tip

    def getOpenHand(self) -> OpenHand:
        return self.openHand

    def getClosedHand(self) -> list[Card]:
        return self.closedHand

    def addTip(self, tip: Tip) -> None:
        self.tip += tip

    def subTip(self, tip: Tip) -> None:
        self.tip -= tip

    def abandonCard(self, abandonCard: Card, addCard: Card) -> None:
        self.closedHand.remove(abandonCard)
        self.closedHand.append(addCard)

    def addOpenHand(self, card: Card) -> None:
        self.openHand.addCard(card)

    def getNonMonopolyCards(self) -> list[Card]:
        return self.openHand.getNonMonopolyCards()

    def getOpenHandCountByCard(self, card: Card) -> int:
        return self.openHand.getOpenHandByCard(card)[0]

    def getAllHandCountByCard(self, card: Card) -> int:
        return self.openHand.getOpenHandByCard(card)[0] + len(list(filter(lambda closedCard: closedCard == card, self.closedHand)))

    def turnMonopolyByCard(self, card: Card, isMonopoly: bool) -> None:
        self.openHand.onMonopoly(card) if isMonopoly else self.openHand.offMonopoly(card)

    def __str__(self) -> str:
        return str(self.openHand) + str(self.tip) + "," + str(self.closedHand[0]) + str(self.closedHand[1]) + str(self.closedHand[2])

class Stock:
    card: Card
    tip: Tip

    def __init__(self, company: Card):
        object.__setattr__(self, "card", company)
        object.__setattr__(self, "tip", Tip(0))

    def getCard(self) -> Card:
        return self.card

    def getTip(self) -> Tip:
        return self.tip

    def addOneTip(self) -> None:
        self.tip += Tip(1)

    def __str__(self) -> str:
        return str(self.card) + str(self.tip).zfill(2)

@dataclass
class Market:
    market: list[Stock]

    def __init__(self):
        object.__setattr__(self, "market", [])

    def getAllStocks(self) -> list[Stock]:
        return self.market

    def getSelectableStocks(self, nonMonopolyCards: list[Card]) -> list[Stock]:
        return list(filter(lambda stock: stock.getCard() in nonMonopolyCards, self.market))

    def getByIndex(self, index: int) -> Stock:
        return self.market.pop(index)

    def putOneTip(self, nonMonopolyCards: list[Card]) -> None:
        list(map(lambda stock: stock.addOneTip(), list(filter(lambda stock: stock.getCard() in nonMonopolyCards, self.market))))

    def addStock(self, card: Card) -> None:
        self.market.append(Stock(card))

    def __str__(self) -> str:
        s = ""
        for stock in self.market:
            s += str(stock) + ","
        return s

@dataclass
class Deck:
    cards: list[Card]

    def __init__(self):
        cards = []
        for _ in range(5):
            cards.append(Card(5))
        for _ in range(6):
            cards.append(Card(6))
        for _ in range(7):
            cards.append(Card(7))
        for _ in range(8):
            cards.append(Card(8))
        for _ in range(9):
            cards.append(Card(9))
        for _ in range(10):
            cards.append(Card(10))

        random.shuffle(cards)

        for _ in range(5):
            cards.pop()

        object.__setattr__(self, "cards", cards)

    def draw(self) -> Card:
        if len(self.cards) == 0:
            raise ValueError("No card.")

        return self.cards.pop()

    def remain(self) -> int:
        return len(self.cards)

@dataclass
class Game:
    playerCount: int
    players: list[Player]
    deck: Deck
    market: Market
    turnCount: int
    record: list[str]

    beforeDrawnCard: Card
    isBeforeDrawnDeck: bool

    DRAW_STRING: ClassVar[str] = "ddd"

    def __init__(self, playerCount: int):
        if playerCount < 3 or playerCount > 7:
            raise ValueError("Wrong player count.")

        deck = Deck()

        players = []
        for _ in range(playerCount):
            players.append(Player([deck.draw(), deck.draw(), deck.draw()]))

        object.__setattr__(self, "deck", deck)
        object.__setattr__(self, "market", Market())
        object.__setattr__(self, "players", players)
        object.__setattr__(self, "playerCount", playerCount)
        object.__setattr__(self, "turnCount", 0)
        object.__setattr__(self, "recordDrawnCard", Card(10))
        object.__setattr__(self, "isBeforeDrawnDeck", False)

        object.__setattr__(self, "record", [])

    def hasDeck(self) -> bool:
        return self.deck.remain() > 0

    def getResult(self) -> list[int]:
        threeTipCounts = [0 for _ in range(self.playerCount)]

        for card in [Card(5), Card(6), Card(7), Card(8), Card(9), Card(10)]:
            counts = list(map(lambda player: player.getAllHandCountByCard(card), self.players))
            maxCount = max(counts)
            maxPlayerCount = len(list(filter(lambda count: count == maxCount, counts)))

            # 最大数のプレイヤーが1人じゃないと何もしない
            if maxPlayerCount != 1:
                continue

            # 最大数じゃない場合は-1をし、その分最大プレイヤーを+3する
            addTip = Tip(0)
            maxPlayerIndex = 0
            for index, player in enumerate(self.players):
                # 最大数を持っているプレイヤーのインデックスを記録
                if counts[index] == maxCount:
                    maxPlayerIndex = index
                    continue

                player.subTip(Tip(counts[index]))
                addTip += Tip(counts[index] * 3)

            self.players[maxPlayerIndex].addTip(addTip)
            threeTipCounts[maxPlayerIndex] += addTip.getCount()

        # print(list(map(lambda player: player.getTip(), self.players)))
        rankData = [
            {
                "index": i,
                "tip": self.players[i].getTip().getCount(),
                "three": threeTipCounts[i],
            }
            for i in range(self.playerCount)
        ]

        sortedRankData = sorted(sorted(sorted(rankData, key = lambda x: x["index"]), key = lambda x: x["three"]), key = lambda x: x["tip"])

        rankPoints = [0 for _ in range(self.playerCount)]
        rankPoints[sortedRankData[-1]["index"]] = 2 # 1位
        rankPoints[sortedRankData[-2]["index"]] = 1 # 2位
        rankPoints[sortedRankData[0]["index"]] = -1 # 最下位

        return rankPoints

    def getGameStatus(self) -> str:
        playerIndex = self.__getPlayerNumber()
        player = self.players[playerIndex]

        maskedRecord = []
        # 他プレイヤーがドローした情報をマスクする
        for index, choice in enumerate(self.record):
            actionPlayerIndex = (index % (self.playerCount * 2)) // 2
            if actionPlayerIndex == playerIndex:
                # 自分の分はマスクしなくていい
                maskedRecord.append(choice)
                continue

            if choice[-1] != "d":
                # ドローじゃない場合はマスクしなくていい
                maskedRecord.append(choice)
                continue

            maskedRecord.append("ddd")

        return {
            "playerIndex": playerIndex,
            "playerCount": self.playerCount,
            "turnCount": self.turnCount,
            "phase": "draw" if self.turnCount % 2 == 0 else "discard",
            "drawAction":
                None if self.turnCount % 2 == 0
                else {
                    "pattern": "deck" if self.record[-1][-1] == "d" else "market",
                    "card": self.record[-1][0],
                },
            "closedHand": list(map(str, player.getClosedHand())),
            "market": list(map(
                lambda stock: {
                    "card": str(stock.getCard()),
                    "tip": str(stock.getTip(),
                )},
                self.market.getAllStocks(),
            )),
            "players": list(map(
                lambda player: {
                    "openHands": {
                        n: {
                            "count": player.getOpenHand().getOpenHandByCard(Card(n))[0],
                            "isMonopoly": player.getOpenHand().getOpenHandByCard(Card(n))[1],
                        }
                        for n in [5, 6, 7, 8, 9, 0]
                    },
                    "tip": str(player.getTip()),
                },
                self.players,
            )),
            "record": maskedRecord,
        }

    def getChoices(self) -> list[str]:
        if self.turnCount % 2 == 0:
            return self.__getDrawChoices()
        else:
            return self.__getDiscardChoices()

    def inputChoiceIndex(self, choiceIndex: int) -> None:
        if self.turnCount % 2 == 0:
            return self.__inputDrawChoices(choiceIndex)
        else:
            return self.__inputDiscardChoices(choiceIndex)

    def __inputDrawChoices(self, choiceIndex: int) -> None:
        player = self.players[self.__getPlayerNumber()]

        choices = self.getChoices()
        if choiceIndex < 0 or choiceIndex >= len(choices):
            raise ValueError("Wrong choice index.")

        if choices[choiceIndex] == self.DRAW_STRING:
            # 山札からドローする場合は、マーケットにチップをおいてから引く
            self.market.putOneTip(player.getNonMonopolyCards())
            # 山札の分1つ引いておく
            player.subTip(Tip(len(choices) - 1))
            self.beforeDrawnCard = self.deck.draw()
            self.isBeforeDrawnDeck = True

            self.record.append(str(self.beforeDrawnCard) + "dd")
        else:
            # マーケットからドローする場合は、ドローしたチップをもらう
            stock = self.market.getByIndex(choiceIndex)
            player.addTip(stock.getTip())
            self.beforeDrawnCard = stock.getCard()
            self.isBeforeDrawnDeck = False

            self.record.append(choices[choiceIndex])

        self.turnCount += 1

    def __inputDiscardChoices(self, choiceIndex: int) -> None:
        player = self.players[self.__getPlayerNumber()]
        choices = self.getChoices()
        if choiceIndex < 0 or choiceIndex >= len(choices):
            raise ValueError("Wrong choice index.")

        # ドローしたものをそのまま使わないときは手札の入れ替え
        if choiceIndex != 3 and choiceIndex != 7:
            player.abandonCard(Card(int(choices[choiceIndex][0])), self.beforeDrawnCard)

        if choiceIndex < 4:
            # 投資する場合
            card = Card(int(choices[choiceIndex][0]))

            # プレイヤーの場に追加
            player.addOpenHand(card)

            # 独禁チップの判定
            counts = list(map(lambda player: player.getOpenHandCountByCard(card), self.players))
            maxCount = max(list(counts))
            maxPlayerCount = len(list(filter(lambda count: count == maxCount, counts)))
            # 単独で最高値を持っていたら独禁チップを設定する
            if maxPlayerCount == 1:
                for index, player in enumerate(self.players):
                    self.players[index].turnMonopolyByCard(card, counts[index] == maxCount)

        else:
            # 捨てる場合はマーケットに追加
            self.market.addStock(Card(int(choices[choiceIndex][0])))

        self.record.append(choices[choiceIndex])
        self.turnCount += 1

    def __getDrawChoices(self) -> list[str]:
        player = self.players[self.__getPlayerNumber()]
        selectableStocks = self.market.getSelectableStocks(player.getNonMonopolyCards())

        # if can draw
        if len(selectableStocks) <= player.getTip().getCount():
            return list(map(str, selectableStocks)) + [self.DRAW_STRING]

        return list(map(str, selectableStocks))

    def __getDiscardChoices(self) -> list[str]:
        player = self.players[self.__getPlayerNumber()]
        cards = player.getClosedHand() + [self.beforeDrawnCard]

        investCard = cards
        # マーケットから引いた数字は捨てることができない
        abandonCard = filter(lambda card: card != self.beforeDrawnCard, cards) if not self.isBeforeDrawnDeck else cards

        return list(map(lambda card: str(card) + "i", investCard)) + list(map(lambda card: str(card) + "a", abandonCard))

    def __getPlayerNumber(self) -> int:
        return (self.turnCount % (self.playerCount * 2)) // 2

    def __str__(self) -> str:
        s = ""
        s += str(self.market) + "\n"
        for player in self.players:
            s += str(player) + "\n"
        s += "".join(self.record)

        return s

game = Game(3)
while game.hasDeck():
    print(game.getGameStatus())

    choices = game.getChoices()
    print(choices)
    choiceIndex = random.randint(0, len(choices) - 1)
    print(choiceIndex)
    game.inputChoiceIndex(choiceIndex)

    print(game.getGameStatus())
    choices = game.getChoices()
    print(choices)
    choiceIndex = random.randint(0, len(choices) - 1)
    print(choiceIndex)
    game.inputChoiceIndex(choiceIndex)

print(game)
print(game.getResult())
