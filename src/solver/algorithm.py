import heapq
from collections import deque
from math import inf
from typing import Callable, Collection

from src.solver.board import State
from src.utils.metric import MockMetric, Metric, RtaMetric


class SearchAlgorithm:
    @classmethod
    def available_algorithms(cls):
        algorithms = {
            'rta': cls.rta_star_search,
            'ida': cls.ida_star_search
        }
        return algorithms

    @staticmethod
    def ida_star_search(initial_state: State, solved: State, VISITOR_FUNC: Callable[..., Collection],
                        HEURISTIC: Callable[..., int], TRANSITION_COST: Callable[..., int] = lambda: 1,
                        metric: Metric = MockMetric()):
        visited_states = {}

        def search(path, g, bound):
            metric.increase_searched_nodes()
            node = path[0]
            f = g + HEURISTIC(node, solved)
            if f > bound:
                return f
            if node.state == solved.state:
                return True
            ret = inf
            moves = VISITOR_FUNC(node, visited_states)
            for m in moves:
                if m not in path:
                    visited_states[m.state] = m
                    path.appendleft(m)
                    t = search(path, g + TRANSITION_COST(), bound)
                    if t is True:
                        return True
                    if t < ret:
                        ret = t
                    path.popleft()
            return ret

        bound = HEURISTIC(initial_state, solved)
        path = deque([initial_state])
        while path:
            t = search(path, TRANSITION_COST(), bound)
            if t is True:
                path.reverse()
                metric.set_path(path)
                return path
            elif t is inf:
                return []
            else:
                bound = t

    @staticmethod
    def rta_star_search(initial_state: State, solved: State, VISITOR_FUNC: Callable[..., Collection],
                        HEURISTIC: Callable[..., int], TRANSITION_COST: Callable[..., int] = lambda: 1,
                        metric: RtaMetric = MockMetric()):
        def minimin(state, visited_states, heuristic, transition_cost):
            successors = VISITOR_FUNC(state, visited_states)

            proccessed_successprs = []

            for move in successors:
                move.cost = heuristic(move, solved) + transition_cost()
                proccessed_successprs.append(move)
            minimal = min(proccessed_successprs, key=lambda x: x.cost)
            return minimal

        def init(initial_state, heuristic, transition_cost):
            successors = VISITOR_FUNC(initial_state, {})
            cost = heuristic(initial_state, solved)
            for move in successors:
                new_cost = heuristic(move, solved)
                if cost > new_cost:
                    cost = new_cost + transition_cost()
            initial_state.cost = cost
            return initial_state

        evaluated = 0
        init = init(initial_state, HEURISTIC, TRANSITION_COST)
        visited_states = {}
        real_time_path = []
        current_state = init
        while current_state.state != solved.state:
            evaluated += 1
            real_time_path.append(current_state)
            metric.increase_searched_nodes()
            visited_states[current_state.state] = current_state
            # print(current_state.state)
            successors = VISITOR_FUNC(current_state, visited_states)
            elems = []

            for successor in successors:
                # Winning state
                if successor.state == solved.state:
                    successor.cost = 0
                    heapq.heappush(elems, (0, successor))
                if successor.cost:
                    heapq.heappush(elems, (successor.cost + TRANSITION_COST(), successor))
                elif successor.state not in visited_states.keys():
                    minimin_result = minimin(successor, visited_states, HEURISTIC, TRANSITION_COST)
                    best = minimin_result
                    successor.cost = best.cost
                    heapq.heappush(elems, (best.cost + TRANSITION_COST(), successor))
                elif not current_state.parent:
                    best = visited_states[successor.state]
                    heapq.heappush(elems, (best.cost + TRANSITION_COST(), best))

            if current_state.parent:
                heapq.heappush(elems, (current_state.parent.cost - TRANSITION_COST(), current_state.parent))

            first_cost, first = heapq.heappop(elems)
            try:
                second_cost, second = heapq.heappop(elems)
            except IndexError:
                second_cost = inf

            if current_state.parent and first.state == current_state.parent.state:
                metric.increase_return_no()

            current_state.cost = second_cost
            current_state = first

        real_time_path.append(current_state)
        metric.set_path(real_time_path)

        visited_states[current_state.state] = current_state
        return (True, real_time_path, {'space': len(real_time_path), 'time': evaluated})
