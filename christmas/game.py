from dataclasses import dataclass
from typing import ClassVar
import itertools
import random
import math

PLAYER_COUNT = 4

@dataclass(frozen=True)
class Card:
    number: int

    def __init__(self, number: int):
        if number < 1 or number > 6:
            raise ValueError("Wrong number.")

        object.__setattr__(self, "number", number)

@dataclass
class Deck:
    cards: list[Card]

    def __init__(self):
        cards = []
        for _ in range(8):
            cards.append(Card(1))
            cards.append(Card(2))
            cards.append(Card(3))
            cards.append(Card(4))
            cards.append(Card(5))
            cards.append(Card(6))

        random.shuffle(cards)

        object.__setattr__(self, "cards", cards)

    def draw(self) -> Card:
        if len(self.cards) == 0:
            raise ValueError("No card.")

        return self.cards.pop().number

def initState(deck):
    # todo PLAYER_COUNT 使う
    return (
        (
            (deck.draw(), 5),
            (deck.draw(), 5),
            (deck.draw(), 5),
            (deck.draw(), 5),
            (deck.draw(), 5),
            (deck.draw(), 5),
            (deck.draw(), 5),
            (deck.draw(), 5),
        ),
        (
            (0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0),
        ),
    )

def turn(deck, state, step):
    if step <= 0 or step > 3:
        raise ValueError("Out of range.")

    remainCardCount = state[0][step][1]
    if remainCardCount == 0:
        raise ValueError("No card.")

    choiceCard = state[0][step][0]
    return (
        (((deck.draw() if remainCardCount >= 1 else 0, remainCardCount - 1), ) + tuple(state[0][i % 8] for i in range(step + 1, step + 8))),
        (state[1][1:] + ((state[1][0][:choiceCard - 1] + (state[1][0][choiceCard - 1] + 1, ) + state[1][0][choiceCard:]), )),
    )

def getChoices(state):
    choices = []
    if state[0][1][1] > 0:
        choices.append(1)
    if state[0][2][1] > 0:
        choices.append(2)
    if state[0][3][1] > 0:
        choices.append(3)

    return choices

def isNotFinish(state):
    count = 0

    for i in range(8):
        if state[0][i][1] == 0:
            count += 1

    return count < 3

def getExpectedPoint(state):
    hands = state[1]
    hand = hands[0]
    table = [0, 2, 5, 10, 20, 32, 45, 60, 80]

    reindeer = 0
    for a, b, c, d in itertools.product(range(hands[0][5] + 1), range(hands[1][5] + 1), range(hands[2][5] + 1), range(hands[3][5] + 1)):
        allCount = hands[0][5] + hands[1][5] + hands[2][5] + hands[3][5]
        probability = (math.comb(hands[0][5], a) * math.comb(hands[1][5], b) * math.comb(hands[2][5], c) * math.comb(hands[3][5], d) * 5 ** (a + b + c + d)) / (6 ** allCount)

        minReindeer = min(
            hands[0][4] + (hands[0][5] - a),
            hands[1][4] + (hands[1][5] - b),
            hands[2][4] + (hands[2][5] - c),
            hands[3][4] + (hands[3][5] - d),
        )
        diffPoint = a * 4 + (-20 if hands[0][4] + (hands[0][5] - a) == minReindeer else 0)

        reindeer += probability * diffPoint

    base = min(hand[0], hand[1], hand[2]) * 10 + table[hand[0]] + table[hand[1]] + table[hand[2]] + hand[3] * 7
    return base + reindeer

deck = Deck()
state = initState(deck)
print(state)

while isNotFinish(state):
    choices = getChoices(state)
    print(choices)
    state = turn(deck, state, choices[random.randint(0, len(choices) - 1)])
    print(state)

point = getExpectedPoint(state)
print(point)


