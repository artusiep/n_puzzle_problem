from src.solver.board import State


class Heuristic:
    @staticmethod
    def hamming(candidate: State, solved: State):
        size = candidate.size
        res = 0
        for i in range(size*size):
            if candidate.state[i] != 0 and candidate.state[i] != solved.state[i]:
                res += 1
        return res

    @staticmethod
    def manhattan(candidate: State, solved: State, size=None):
        if not size:
            size = candidate.size
        res = 0
        for i in range(size*size):
            if candidate.state[i] != 0 and candidate.state[i] != solved.state[i]:
                ci = solved.state.index(candidate.state[i])
                y = (i // size) - (ci // size)
                x = (i % size) - (ci % size)
                res += abs(y) + abs(x)
        return res

    @classmethod
    def available_heuristics(cls):
        heuristics = {
            'manhattan': cls.manhattan,
            'hamming': cls.hamming
        }
        return heuristics