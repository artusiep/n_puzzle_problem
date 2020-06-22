from src.solver.algorithm import ida_star_search
from src.solver.board import UnsolvedPuzzle, PuzzleSolution, Puzzle
from src.solver.heuristics import Heuristic


class Game:
    def __init__(self, initial_state: UnsolvedPuzzle, result_state: PuzzleSolution):
        self.initial_state = initial_state
        self.result_state = result_state

    def run(self, display):
        result = self.solve(ida_star_search, Heuristic.manhattan)
        if self._check_win(result[1][-1]):
            if display:
                path = [Puzzle.get_board_flat(Puzzle, x, 'x') for x in result[1]]
                [print(node.formatted_puzzle, '\n---') for node in path]
            print(result[2])
        else:
            print(f"""Finding solution failed. 
Initial state: 
{self.initial_state.formatted_puzzle}
Solution state
{self.result_state.formatted_puzzle}
""")

    def analise_states(self):
        pass

    def solve(self, search_algorithm, heuristic):
        return search_algorithm(self.initial_state, self.result_state, heuristic, 1)

    def _check_win(self, result_board):
        return self.result_state.flat_board == result_board
