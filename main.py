from src.board import Puzzle, UnsolvedPuzzle, PuzzleSolution
from src.game import Game

unsolved_puzzle = Puzzle.get_board_from_csv(UnsolvedPuzzle, "samples/sample8/initial.csv", "x")
puzzle_solution = Puzzle.get_board_from_csv(PuzzleSolution, "samples/sample8/result.csv", "x")
game = Game(unsolved_puzzle, puzzle_solution)
game.run(True)


