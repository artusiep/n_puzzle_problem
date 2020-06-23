import copy
import glob
import os
import random

from src.solver.board import Puzzle, UnsolvedPuzzle
from src.solver.game import Game


class Action:
    @staticmethod
    def solve(args):
        if args.batch:
            Action.solve_batch(args)
        else:
            Action.solve_single(args)

    @staticmethod
    def solve_single(args):
        unsolved_puzzle = Puzzle.get_board_from_file(UnsolvedPuzzle, args.init_file, args.blank_char)
        if unsolved_puzzle.is_solvable(args.blank_char, args.final_state):
            puzzle_solution = Puzzle.generate_solution(unsolved_puzzle, args.final_state, args.blank_char)
            game = Game(unsolved_puzzle, puzzle_solution)
            game.run(True)
        else:
            print("Initial state is not solvable")
            print(unsolved_puzzle.formatted_puzzle)

    @staticmethod
    def solve_batch(args):
        result = []
        os.chdir(args.batch)
        for filename in glob.glob("*.puzzle"):
            unsolved_puzzle = Puzzle.get_board_from_csv(UnsolvedPuzzle, filename, args.blank_char)
            if unsolved_puzzle.is_solvable(args.blank_char, args.final_state):
                puzzle_solution = Puzzle.generate_solution(unsolved_puzzle, args.final_state, args.blank_char)
                game = Game(unsolved_puzzle, puzzle_solution)
                result.append(game.run(False))
            else:
                print("Initial state is not solvable")
                print(unsolved_puzzle.formatted_puzzle)
        metrics = [r[2] for r in result]
        print(sum([metric['time'] for metric in metrics]) / len(metrics))

    @staticmethod
    def generate(args):
        def shuffle_puzzle(reference_puzzle: UnsolvedPuzzle):
            reference_puzzle_copy = copy.deepcopy(reference_puzzle)
            for _ in range(random.randint(5, 50)):
                reference_puzzle_copy.move(random.choice(reference_puzzle_copy.available_moves))
            return reference_puzzle_copy

        reference_puzzle = Puzzle.get_board_from_file(UnsolvedPuzzle, args.reference_file, args.blank_char)
        for x in range(args.number):
            shuffled_puzzle = shuffle_puzzle(reference_puzzle)
            path = f'{args.destination}/puzzle{shuffled_puzzle.size ** 2 - 1}/'
            os.makedirs(path, exist_ok=True)
            with open(f'{path}/{id(shuffled_puzzle)}.puzzle', 'w') as f:
                f.write(shuffled_puzzle.csv_puzzle)
            with open(f'{path}/solution.puzzle', 'w') as f:
                f.write(reference_puzzle.csv_puzzle)
