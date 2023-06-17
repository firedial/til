class TCSetting:
    V_MAIN = 128
    V_HAND = 129
    V_BOOL = 130
    V_SPEND = 132
    V_MIN_TIME = 133

    def __init__(self, data):
        self.data = data
        self.v = [0 for _ in range(256)]
        self.commitedDiffTime = 0

    def main(self):
        return self.v[self.V_MAIN]

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
        self.v[self.V_SPEND] = 0
        self.process(self.data["start"])

    def turnProcess(self, diffFloatTime: float):
        self.loopStartProcess(self.diffTime(diffFloatTime))
        self.process(self.data["turn"])

    def turnEndProcess(self):
        self.process(self.data["end"])

    def overProcess(self):
        self.process(self.data["over"])

    def process(self, process):
        for c in process:
            match c:
                case (_, _, _, "if") | (_, _, _, _, _, "if"):
                    if self.v[self.V_BOOL] != 0:
                        self.eval(c[:-1])
                case _:
                    self.eval(c)

    def eval(self, c):
        v = lambda x: x if type(x) is int else self.v[int(x[1:])]
        match c:
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
