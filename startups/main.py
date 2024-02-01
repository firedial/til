from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Card:
    number: int

    def __init__(self, number: int):
        if number < 5 or number > 10:
            raise ValueError("Wrong company number.")

        object.__setattr__(self, "number", number)

    def getNumber(self) -> int:
        return self.number

@dataclass
class Tip:
    count: int

    def __init__(self, count: int):
        if count < 0:
            raise ValueError("Wrong tip count.")

        object.__setattr__(self, "count", count)

    def getCount(self) -> int:
        return self.count

@dataclass
class OpenHand:
    companies: list[tuple[int, bool]]

    def __init__(self):
        object.__setattr__(self, "companies", [(0, False) for _ in range(6)])

    def addCard(self, card: Card) -> None:
        self.companies[card.getNumber() - 5] = (self.companies[card.getNumber() - 5][0] + 1, self.companies[card.getNumber() - 5][1])

    def onMonopoly(self, card: Card) -> None:
        self.companies[card.getNumber() - 5] = (self.companies[card.getNumber() - 5][0], True)

    def offMonopoly(self, card: Card) -> None:
        self.companies[card.getNumber() - 5] = (self.companies[card.getNumber() - 5][0], False)

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

@dataclass
class OpenPlace:
    openPlace: list[tuple[Card, Tip]]

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
    turnCount: int
    record: str

    def __init__(self, playerCount: int):
        if playerCount < 3 or playerCount > 7:
            raise ValueError("Wrong player count.")

        deck = Deck()

        players = []
        for _ in range(playerCount):
            players.append(Player([deck.draw(), deck.draw(), deck.draw()]))

        object.__setattr__(self, "deck", deck)
        object.__setattr__(self, "players", players)
        object.__setattr__(self, "playerCount", playerCount)
        object.__setattr__(self, "turnCount", 0)
        object.__setattr__(self, "record", "")

    def getChoices(self) -> list[str]:
        if self.turnCount % 2 == 0:
            return self.__getDrawChoices()
        else:
            return self.__getDiscardChoices()

    def inputChoiceIndex(self, choiceIndex: int) -> list[str]:
        choices = self.getChoices()
        if choiceIndex < 0 or choiceIndex >= len(choices):
            raise ValueError("Wrong choice index.")

        self.record += choices[choiceIndex]
        self.turnCount += 1

    def __getDrawChoices(self) -> list[str]:
        return ["a", "c"]

    def __getDiscardChoices(self) -> list[str]:
        return ["b"]

game = Game(3)
game.inputChoiceIndex(1)
game.inputChoiceIndex(0)
game.inputChoiceIndex(0)
print(game)