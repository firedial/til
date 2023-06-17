import keyboard
import time
import TCSetting


aData = {
    "init": [("v133", "=", 1), ("v128", "=", 30)],
    "start": [],
    "turn": [],
    "end": [("v132", "<", 30), ("v64", "=", 30, "-", "v132", "if"), ("v128", "=", "v128", "+", "v64", "if")],
    "over": [],
}

bData = {
    "init": [("v133", "=", 1), ("v128", "=", 30)],
    "start": [],
    "turn": [],
    "end": [("v132", "<", 30), ("v64", "=", 30, "-", "v132", "if"), ("v128", "=", "v128", "+", "v64", "if")],
    "over": [],
}

playerData = [TCSetting.TCSetting(aData), TCSetting.TCSetting(bData)]
playerData[0].initProcess()
playerData[1].initProcess()

while True:
    if keyboard.is_pressed("a"):
        turn = 1
        break
    if keyboard.is_pressed("b"):
        turn = 0
        break

turnStartTime = time.perf_counter()
data = playerData[turn]
data.turnStartProcess()

while True:
    time.sleep(0.1)
    print(playerData[0].main(), playerData[1].main())

    loopStartTime = time.perf_counter()
    data.turnProcess(loopStartTime - turnStartTime)

    if (keyboard.is_pressed("a") and turn == 0) or (keyboard.is_pressed("b") and turn == 1):
        data.turnEndProcess()
        turn ^= 1

        turnStartTime = time.perf_counter()
        data = playerData[turn]
        data.turnStartProcess()

    if data.main() <= 0:
        data.overProcess()
        if data.main() <= 0:
            print(f"turn {turn} is lose")
            break
