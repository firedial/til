class TCSetting:
    V_MAIN = 128
    V_HAND = 129
    V_BOOL = 130
    V_FINISH = 131
    V_SPEND = 132
    V_MIN_TIME = 133
    V_RETURN = 134

    def __init__(self, data):
        self.data = data
        self.v = [0 for _ in range(256)]
        self.commitedDiffTime = 0
        self.diffFloatTime = 0.0

    def isFinished(self):
        return self.v[self.V_FINISH] != 0

    def setFinished(self):
        self.v[self.V_FINISH] = 1

    def main(self):
        return self.v[self.V_MAIN]

    def mainDisplay(self):
        colon = ":" if int(self.diffFloatTime * 2) % 2 == 0 else " "
        if self.main() < 60:
            return "00" + colon + str(self.main()).zfill(2)
        elif self.main() < 3600:
            return str(self.main() // 60).zfill(2) + colon + str(self.main() % 60).zfill(2)
        else:
            return str(self.main() // 3600).zfill(2) + colon + str((self.main() % 3600) // 60).zfill(2)

    def diffTime(self, diff: float):
        return (int(diff) // self.v[self.V_MIN_TIME]) * self.v[self.V_MIN_TIME]

    def loopStartProcess(self, diffTime: int):
        self.v[self.V_SPEND] = diffTime
        uncommitedDiffTime = diffTime - self.commitedDiffTime
        if uncommitedDiffTime > 0:
            self.v[self.V_MAIN] -= uncommitedDiffTime
            self.commitedDiffTime = diffTime

    def initProcess(self):
        self.process(self.data["init"])

    def turnStartProcess(self):
        self.commitedDiffTime = 0
        self.v[self.V_HAND] += 1
        self.process(self.data["start"])

    def turnProcess(self, diffFloatTime: float):
        self.diffFloatTime = diffFloatTime
        self.loopStartProcess(self.diffTime(diffFloatTime))
        self.process(self.data["turn"])

    def turnEndProcess(self):
        self.v[self.V_SPEND] = 0
        self.process(self.data["end"])

    def overProcess(self):
        self.process(self.data["over"])

    def process(self, process):
        for c in process:
            if self.v[self.V_RETURN]:
                break

            if c[-1] == "if":
                if self.v[self.V_BOOL] != 0:
                    self.eval(c[:-1])
            else:
                self.eval(c)

    def eval(self, c):
        v = lambda x: x if type(x) is int else self.v[int(x[1:])]
        match c:
            case ("finish",):
                self.v[self.V_FINISH] = 1
                self.v[self.V_RETURN] = 1
            case ("return",):
                self.v[self.V_RETURN] = 1
            case (_, "<", _):
                self.v[self.V_BOOL] = 1 if v(c[0]) < v(c[2]) else 0
            case (_, ">", _):
                self.v[self.V_BOOL] = 1 if v(c[0]) > v(c[2]) else 0
            case (_, "<=", _):
                self.v[self.V_BOOL] = 1 if v(c[0]) <= v(c[2]) else 0
            case (_, ">=", _):
                self.v[self.V_BOOL] = 1 if v(c[0]) >= v(c[2]) else 0
            case (_, "==", _):
                self.v[self.V_BOOL] = 1 if v(c[0]) == v(c[2]) else 0
            case (_, "!=", _):
                self.v[self.V_BOOL] = 1 if v(c[0]) != v(c[2]) else 0
            case (_, "&&", _):
                self.v[self.V_BOOL] = 1 if bool(v(c[0])) and bool(v(c[2])) else 0
            case (_, "||", _):
                self.v[self.V_BOOL] = 1 if bool(v(c[0])) or bool(v(c[2])) else 0
            case ("!", _):
                self.v[self.V_BOOL] = 1 if not bool(v(c[0])) else 0
            case (_, "=", _):
                self.v[int(c[0][1:])] = v(c[2])
            case (_, "=", _, "+", _):
                self.v[int(c[0][1:])] = v(c[2]) + v(c[4])
            case (_, "=", _, "-", _):
                self.v[int(c[0][1:])] = v(c[2]) - v(c[4])
            case (_, "=", _, "*", _):
                self.v[int(c[0][1:])] = v(c[2]) * v(c[4])
            case (_, "=", _, "//", _):
                self.v[int(c[0][1:])] = v(c[2]) // v(c[4])
            case (_, "=", _, "%", _):
                self.v[int(c[0][1:])] = v(c[2]) % v(c[4])
