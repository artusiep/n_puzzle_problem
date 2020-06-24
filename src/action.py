import copy
import glob
import os
import random

from src.solver.board import Puzzle, UnsolvedPuzzle
from src.solver.game import Game
from src.utils.progress_bar import print_progress_bar


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
            result = game.run(args.algorithm, args.heuristic)
            print(result)
        else:
            print("Initial state is not solvable")
            print(unsolved_puzzle.formatted_puzzle)

    @staticmethod
    def solve_batch(args):
        result = []
        os.chdir(args.batch)
        files = glob.glob("*.puzzle")
        print_progress_bar(0, len(files), prefix='Progress:', suffix='Complete', length=50)
        for i, filename in enumerate(files):
            unsolved_puzzle = Puzzle.get_board_from_csv(UnsolvedPuzzle, filename, args.blank_char)
            if unsolved_puzzle.is_solvable(args.blank_char, args.final_state):
                puzzle_solution = Puzzle.generate_solution(unsolved_puzzle, args.final_state, args.blank_char)
                game = Game(unsolved_puzzle, puzzle_solution)
                result.append(game.run(False))
            else:
                print("Initial state is not solvable")
                print(unsolved_puzzle.formatted_puzzle)
            print_progress_bar(i+1, len(files), prefix='Progress:', suffix='Complete', length=50)
        print(Game.get_report(result))

    @staticmethod
    def generate(args):
        def shuffle_puzzle(reference_puzzle: UnsolvedPuzzle):
            reference_puzzle_copy = copy.deepcopy(reference_puzzle)
            for _ in range(random.randint(50, 150)):
                reference_puzzle_copy.move(random.choice(reference_puzzle_copy.available_moves))
            return reference_puzzle_copy

        reference_puzzle = Puzzle.get_board_from_file(UnsolvedPuzzle, args.reference_file, args.blank_char)
        path = f'{args.destination}/puzzle{reference_puzzle.size ** 2 - 1}/'
        for no in range(args.number):
            shuffled_puzzle = shuffle_puzzle(reference_puzzle)
            os.makedirs(path, exist_ok=True)
            with open(f'{path}/{no}-{id(shuffled_puzzle)}.puzzle', 'w') as f:
                f.write(shuffled_puzzle.csv_puzzle)
        with open(f'{path}/puzzle.solution', 'w') as f:
            f.write(reference_puzzle.csv_puzzle)
