from src.board import Puzzle, UnsolvedPuzzle, PuzzleSolution
from src.game import Game

unsolved_puzzle = Puzzle.get_board_from_csv(UnsolvedPuzzle, "sample24/initial.csv", "x")
puzzle_solution = Puzzle.get_board_from_csv(PuzzleSolution, "sample24/result.csv", "x")
game = Game(unsolved_puzzle, puzzle_solution)
game.make_step(True)
print("===================")
game.make_step(True)
print("===================")
game.make_step(True)
print("===================")
game.make_step(True)
print("===================")
game.make_step(True)
print("===================")
