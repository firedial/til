from dataclasses import dataclass
from typing import ClassVar
import random


@dataclass(frozen=True)
class Card:
    number: int

    def __init__(self, number: int):
        if number < 5 or number > 10:
            raise ValueError("Wrong company number.")

        object.__setattr__(self, "number", number)

    def __str__(self) -> str:
        return str(number % 10)

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
        return self.__init__(self.count + other.count)

    def __sub__(self, other):
        return self.__init__(self.count - other.count)

    def __str__(self) -> str:
        return str(count)

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

    def onMonopoly(self, card: Card) -> None:
        self.companies[card] = (self.companies[card][0], True)

    def offMonopoly(self, card: Card) -> None:
        self.companies[card] = (self.companies[card][0], False)

    def getNonMonopolyCards(self) -> list[Card]:
        return list(dict((filter(lambda company: not company[1][1], self.companies.items()))))

@dataclass
class Player:
    closedHand: list[Card]
    openHand: OpenHand
    tip: Tip
    drawCard: Card | None

    def __init__(self, cards: list[Card]):
        if len(cards) != 3:
            raise ValueError("Wrong cards count.")

        object.__setattr__(self, "openHand", OpenHand())
        object.__setattr__(self, "closedHand", cards)
        object.__setattr__(self, "tip", Tip(10))
        object.__setattr__(self, "drawCard", None)

    def getTip(self) -> Tip:
        return self.tip

    def addTip(self, tip: Tip) -> None:
        self.tip += tip

    def subTip(self, tip: Tip) -> None:
        self.tip -= tip

    def getNonMonopolyCards(self) -> list[Card]:
        return self.openHand.getNonMonopolyCards()

    def setDrawCard(self, card: Card) -> None:
        self.drawCard = card

class Stock:
    card: Card
    tip: Tip

    def __init__(self, company: Card):
        object.__setattr__(self, "company", company)
        object.__setattr__(self, "value", Tip(0))

    def getCard(self) -> Card:
        return self.card

    def __str__(self) -> str:
        return str(self.card) + str(self.Tip).zfill(2)

@dataclass
class Market:
    market: list[Stock]

    def __init__(self):
        object.__setattr__(self, "market", [])

class Stock:
    card: Card
    tip: Tip

    def __init__(self, company: Card):
        object.__setattr__(self, "company", company)
        object.__setattr__(self, "value", Tip(0))

    def getCard(self) -> Card:
        return self.card

    def getTip(self) -> Tip:
        return self.tip

    def addOneTip(self) -> None:
        self.tip += Tip(1)

    def __str__(self) -> str:
        return str(self.card) + str(self.Tip).zfill(2)

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
        map(lambda stock: stock.addOneTip(), filter(lambda stock: stock.getCard() in nonMonopolyCards, self.market))


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
        object.__setattr__(self, "record", "")

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
            player.setDrawCard(self.deck.draw())
        else:
            # マーケットからドローする場合は、ドローしたチップをもらう
            stock = self.market.getByIndex(choiceIndex)
            player.addTip(stock.getTip())
            player.setDrawCard(stock.getCard())

        self.record += choices[choiceIndex]
        self.turnCount += 1

    def __inputDiscardChoices(self, choiceIndex: int) -> None:
        pass

    def __getDrawChoices(self) -> list[str]:
        player = self.players[self.__getPlayerNumber()]
        selectableStocks = self.market.getSelectableStocks(player.getNonMonopolyCards())

        # if can draw
        if len(selectableStocks) <= player.getTip().getCount():
            return list(map(str, selectableStocks)) + [self.DRAW_STRING]

        return list(map(str, selectableStocks))

    def __getDiscardChoices(self) -> list[str]:
        return ["b"]

    def __getPlayerNumber(self) -> int:
        return (self.turnCount % (self.playerCount * 2)) // 2

game = Game(3)
game.inputChoiceIndex(0)
game.inputChoiceIndex(0)
game.inputChoiceIndex(0)
print(game)
