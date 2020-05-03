import random

from src.board import UnsolvedPuzzle, PuzzleSolution
from src.direction import Direction


class Game:
    def __init__(self, unsolved_puzzle: UnsolvedPuzzle, puzzle_solution: PuzzleSolution):
        self.unsolved_puzzle = unsolved_puzzle
        self.puzzle_solution = puzzle_solution

    def make_step(self, display):
        direction = random.choice(self.unsolved_puzzle.available_moves)
        self.unsolved_puzzle.move(direction)
        if self._check_win():
            return "You Won" # Right now I don't have clue how it will be implemented
        if display:
            print(self.unsolved_puzzle.formatted_puzzle)

    def _check_win(self):
        return self.unsolved_puzzle == self.puzzle_solution
