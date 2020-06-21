import random

from src.algorithm import ida_star_search
from src.board import UnsolvedPuzzle, PuzzleSolution, Puzzle
from src.direction import Direction
from src.heuristics import Heuristic


class Game:
    def __init__(self, unsolved_puzzle: UnsolvedPuzzle, puzzle_solution: PuzzleSolution):
        self.unsolved_puzzle = unsolved_puzzle
        self.puzzle_solution = puzzle_solution

    def run(self, display):
        result = self.solve(ida_star_search, Heuristic.manhattan)
        if self._check_win(result[1][-1]):
            pass
            # return "You Won" # Right now I don't have clue how it will be implemented
        if display:
            path = [Puzzle.get_board_flat(Puzzle, x, 'x')for x in result[1]]
            [print(node.formatted_puzzle, '\n') for node in path]


    def analise_states(self):
        pass

    def solve(self, search_algorithm, heuristic):
        return search_algorithm(self.unsolved_puzzle, self.puzzle_solution, heuristic, 1)


    def _check_win(self, result_board):
        return self.puzzle_solution.flat_board == result_board
