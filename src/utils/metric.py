import time

from src.solver.heuristics import Heuristic


class Metric:
    def __init__(self):
        self.init_hamming = 0
        self.init_manhattan = 0
        self.search_alg = 0
        self.heuristic = None
        self.time = 0
        self.time_start = None
        self.searched_nodes = 0
        self.time_per_node = 0
        self.path = 0
        self.nodes_no = 0

    def calc_heuristics(self, canidate, solved):
        self.init_hamming = Heuristic.hamming(canidate, solved)
        self.init_manhattan = Heuristic.manhattan(canidate, solved)

    def set_search_alg(self, alg):
        self.search_alg = alg

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic

    def increase_searched_nodes(self):
        self.searched_nodes += 1
        return self.searched_nodes

    def set_path(self, path):
        self.path = path
        return self.path

    def increase_nodes_no(self):
        self.nodes_no += 1
        return self.nodes_no

    def timer_start(self):
        self.time_start = time.perf_counter()

    def timer_stop(self):
        self.time = time.perf_counter() - self.time_start

    def timer_reset(self):
        self.time = 0

    def __set_time(self, time):
        self.time = time


class RtaMetric(Metric):
    def __init__(self):
        super().__init__()
        self.return_no = 0

    def increase_return_no(self):
        self.return_no += 1
        return self.return_no


class MockMetric(RtaMetric):
    def __init__(self):
        pass

    def calc_heuristics(self, canidate, solved):
        pass

    def set_sorting_alg(self, alg):
        pass

    def increase_searched_nodes(self):
        pass

    def set_path(self, path):
        pass

    def increase_nodes_no(self):
        pass

    def timer_start(self):
        pass

    def timer_stop(self):
        pass

    def timer_reset(self):
        pass

    def __set_time(self, time):
        pass

    def increase_return_no(self):
        pass