import json
import time

from src.solver.heuristics import Heuristic


class Metric:
    def __init__(self):
        self.init_state = None
        self.solution_state = None
        self.init_hamming = 0
        self.init_manhattan = 0
        self.search_alg = 0
        self.heuristic = None
        self.time = 0
        self.time_start = None
        self.searched_nodes = 0
        self.time_per_node = 0
        self.path = 0
        self.paths_nodes_no = 0

    def init(self, canidate, solved):
        self.init_state = canidate.state
        self.solution_state = solved.state
        self.init_hamming = Heuristic.hamming(canidate, solved)
        self.init_manhattan = Heuristic.manhattan(canidate, solved)

    def set_search_alg(self, alg):
        self.search_alg = alg

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic

    def increase_searched_nodes(self):
        self.searched_nodes += 1

    def set_path(self, path):
        self.path = path
        self.paths_nodes_no = len(path)

    def timer_start(self):
        self.time_start = time.perf_counter()

    def timer_stop(self):
        self.time = time.perf_counter() - self.time_start
        try:
            self.time_per_node = self.time / self.searched_nodes
        except ZeroDivisionError:
            self.time_per_node = 0

    def timer_reset(self):
        self.time_per_node = 0
        self.time = 0

    def __set_time(self, time):
        self.time = time

    def summary_to_file(self, file, with_path=False):
        if with_path:
            self.path = [x.state for x in self.path]
        else:
            self.path = None
        json.dump(self.__dict__, file)

    def summary_to_console(self, with_path=False):
        if with_path:
            self.path = [x.state for x in self.path]
        else:
            self.path = None
        print(json.dumps(self.__dict__))


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

    def set_search_alg(self, alg):
        return

    def set_heuristic(self, heuristic):
        return

    def increase_searched_nodes(self):
        return

    def set_path(self, path):
        return

    def timer_start(self):
        return

    def timer_stop(self):
        return

    def timer_reset(self):
        return

    def __set_time(self, time):
        return

    def summary_to_file(self, file, with_path=False):
        return

    def summary_to_console(self, with_path=False):
        return

    def increase_return_no(self):
        return
