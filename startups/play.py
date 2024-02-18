from game import RoundGame
import concurrent.futures
import random

def roundPlay(playerChoiceFunctions):
    game = RoundGame(playerChoiceFunctions)
    return game.play()

def playerA(status):
    choices = status["choices"]
    if status["phase"] == "draw":
        return random.randint(0, len(choices) - 1)
    else:
        return random.randint(0, len(choices) - 1)

def playerB(status):
    choices = status["choices"]
    if status["phase"] == "draw":
        return random.randint(0, len(choices) - 1)
    else:
        return random.randint(0, len(choices) - 1)

def playerC(status):
    choices = status["choices"]
    if status["phase"] == "draw":
        return random.randint(0, len(choices) - 1)
    else:
        return random.randint(0, len(choices) - 1)

playerChoiceFunctions = [
    playerA,
    playerB,
    playerC,
]
playerCount = len(playerChoiceFunctions)
results = [[0 for _ in range(playerCount)] for _ in range(playerCount)]
count = 10000

with concurrent.futures.ProcessPoolExecutor() as executor:
    futures = [executor.submit(roundPlay, playerChoiceFunctions) for _ in range(count)]

    for future in concurrent.futures.as_completed(futures):
        gameResult = future.result()
        for index, rank in enumerate(gameResult):
            results[index][rank - 1] += 1

print(results)
for result in results:
    print(result[0] / count)
