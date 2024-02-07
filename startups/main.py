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
        if count < 0 or count > 70:
            raise ValueError("Wrong tip count.")

        object.__setattr__(self, "count", count)

    def getCount(self) -> int:
        return self.count

    def addCount(self, tip: int) -> None:
        if self.count + tip > 70:
            raise ValueError("Wrong tip count.")

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

    def getOpenHandCountByCard(self, card: Card) -> tuple[int, bool]:
        return self.openHand.getOpenHandByCard(card)[0]

    def turnMonopolyByCard(self, card: Card, isMonopoly: bool) -> None:
        self.openHand.onMonopoly(card) if isMonopoly else self.openHand.offMonopoly(card)

    def __str__(self) -> str:
        return str(self.openHand) + str(self.tip)

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
    record: str

    beforeDrawnCard: Card | None
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
        object.__setattr__(self, "recordDrawnCard", None)
        object.__setattr__(self, "isBeforeDrawnDeck", False)

        object.__setattr__(self, "record", "")

    def hasDeck(self) -> bool:
        return self.deck.remain() > 0

    def getResult(self) -> list[int]:
        pass

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
        else:
            # マーケットからドローする場合は、ドローしたチップをもらう
            stock = self.market.getByIndex(choiceIndex)
            player.addTip(stock.getTip())
            self.beforeDrawnCard = stock.getCard()
            self.isBeforeDrawnDeck = False

        self.record += choices[choiceIndex]
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

        self.record += choices[choiceIndex]
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

        return s

game = Game(3)
while game.hasDeck():
    print(game)

    choices = game.getChoices()
    print(choices)
    choiceIndex = random.randint(0, len(choices) - 1)
    print(choiceIndex)
    game.inputChoiceIndex(choiceIndex)

    choices = game.getChoices()
    print(choices)
    choiceIndex = random.randint(0, len(choices) - 1)
    print(choiceIndex)
    game.inputChoiceIndex(choiceIndex)

