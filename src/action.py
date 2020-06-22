from src.solver.board import Puzzle, UnsolvedPuzzle
from src.solver.game import Game


class Action:
    @staticmethod
    def solve(args):
        unsolved_puzzle = Puzzle.get_board_from_file(UnsolvedPuzzle, args.init_file, args.blank_char)
        if unsolved_puzzle.is_solvable(args.blank_char, args.final_state):
            puzzle_solution = Puzzle.generate_solution(unsolved_puzzle, args.final_state, args.blank_char)
            game = Game(unsolved_puzzle, puzzle_solution)
            game.run(True)
        else:
            print("Initial state is not solvable")
            print(unsolved_puzzle.formatted)

    @staticmethod
    def generate(args):
        pass
