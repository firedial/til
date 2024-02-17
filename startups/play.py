from game import Game
import concurrent.futures
import random

def playerDA(choices):
    return random.randint(0, len(choices) - 1)

def playerDB(choices):
    return 0

def playerDC(choices):
    return 0
    return random.randint(0, len(choices) - 1)
    return len(choices) - 1

def playerAA(choices):
    return random.randint(0, len(choices) - 1)

def playerAB(choices):
    return len(choices) - 1
    return random.randint(0, len(choices) - 1)

def playerAC(choices):
    return len(choices) - 1
    return random.randint(0, len(choices) - 1)

def play(players):
    game = Game(3)
    count = 0

    while game.hasDeck():
        choices = game.getChoices()
        match players[count % 3]:
            case 0:
                choiceIndex = playerDA(choices)
            case 1:
                choiceIndex = playerDB(choices)
            case 2:
                choiceIndex = playerDC(choices)
        game.inputChoiceIndex(choiceIndex)

        choices = game.getChoices()
        match players[count % 3]:
            case 0:
                choiceIndex = playerAA(choices)
            case 1:
                choiceIndex = playerAB(choices)
            case 2:
                choiceIndex = playerAC(choices)
        game.inputChoiceIndex(choiceIndex)

        count += 1

    gameResult = game.getResult()
    result = [0, 0, 0]
    result[players[0]] = gameResult[0]
    result[players[1]] = gameResult[1]
    result[players[2]] = gameResult[2]

    return result

def roundPlay():
    point = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    players = [0, 1, 2]
    random.shuffle(players)

    for _ in range(4):
        result = play(players)
        minPlayerIndex = -1
        for index, value in enumerate(result):
            match value:
                case 2:
                    point[index][0] += 1
                case 1:
                    point[index][1] += 1
                case -1:
                    point[index][2] += 1
                    minPlayerIndex = index

        # 最下位のプレイヤーを最初にする
        while True:
            if players[0] == minPlayerIndex:
                break

            players.append(players.pop(0))

    return result


result = [0, 0, 0]
with concurrent.futures.ProcessPoolExecutor() as executor:
    futures = [executor.submit(roundPlay) for _ in range(5)]

    for future in concurrent.futures.as_completed(futures):
        gameResult = future.result()
        result[0] += gameResult[0]
        result[1] += gameResult[1]
        result[2] += gameResult[2]

print(result)
