from src.solver.algorithm import SearchAlgorithm
from src.solver.board import UnsolvedPuzzle, PuzzleSolution, State
from src.solver.heuristics import Heuristic
from src.utils.metric import Metric, RtaMetric


class Game:
    EMPTY_TILE = 'x'

    def __init__(self, initial_state: UnsolvedPuzzle, result_state: PuzzleSolution):
        self.initial_state = initial_state
        self.result_state = result_state

    def run(self, algorithm, heuristic, metrics):
        if algorithm == 'rta':
            metric_collector = RtaMetric()
        else:
            metric_collector = Metric()
        metric_collector.init(self.initial_state, self.result_state)

        algorithm_func = SearchAlgorithm.available_algorithms()[algorithm]
        heuristic_func = Heuristic.available_heuristics()[heuristic]

        metric_collector.set_search_alg(algorithm)
        metric_collector.set_heuristic(heuristic)

        metric_collector.timer_start()
        result = self.solve(algorithm_func, heuristic_func, metric_collector, metrics)
        metric_collector.timer_stop()

        return result, metric_collector

    @staticmethod
    def clone_and_swap(data, y0, y1):
        clone = list(data)
        tmp = clone[y0]
        clone[y0] = clone[y1]
        clone[y1] = tmp
        return tuple(clone)

    @staticmethod
    def choose_next_move(element, size, parent, visited):
        if element in visited.keys():
            return visited[element]
        else:
            return State(element, size, parent=parent)

    @staticmethod
    def possible_moves(state, visited):
        res = []
        y = state.state.index(Game.EMPTY_TILE)
        size = state.size
        if y % size > 0:
            left = Game.clone_and_swap(state.state, y, y - 1)
            res.append(Game.choose_next_move(left, size, state, visited))
        if y % size + 1 < size:
            right = Game.clone_and_swap(state.state, y, y + 1)
            res.append(Game.choose_next_move(right, size, state, visited))
        if y - size >= 0:
            up = Game.clone_and_swap(state.state, y, y - size)
            res.append(Game.choose_next_move(up, size, state, visited))
        if y + size < len(state.state):
            down = Game.clone_and_swap(state.state, y, y + size)
            res.append(Game.choose_next_move(down, size, state, visited))
        return res

    def solve(self, search_algorithm, heuristic, metric_collector, metrics):
        if metrics:
            search_result = search_algorithm(self.initial_state, self.result_state, Game.possible_moves, heuristic,
                                             metric=metric_collector)
        else:
            search_result = search_algorithm(self.initial_state, self.result_state, Game.possible_moves, heuristic)
        return search_result
