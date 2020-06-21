import itertools


class Heuristic:
    @staticmethod
    def hamming(candidate, solved, size): #aka tiles out of place
        res = 0
        for i in range(size*size):
            if candidate[i] != 0 and candidate[i] != solved[i]:
                res += 1
        return res

    @staticmethod
    def manhattan(candidate, solved, size):
        res = 0
        for i in range(size*size):
            if candidate[i] != 0 and candidate[i] != solved[i]:
                ci = solved.index(candidate[i])
                y = (i // size) - (ci // size)
                x = (i % size) - (ci % size)
                res += abs(y) + abs(x)
        return res