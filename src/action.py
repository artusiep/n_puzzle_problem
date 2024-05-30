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
        Game.EMPTY_TILE = args.blank_char
        if args.batch:
            Action.__solve_batch(args)
        else:
            Action.__solve_single(args)

    @staticmethod
    def __solve_single(args):
        unsolved_puzzle = Puzzle.get_board_from_file(UnsolvedPuzzle, args.init_file, args.blank_char)
        if unsolved_puzzle.is_solvable(args.blank_char, args.final_state):
            Action.__solve_core(unsolved_puzzle, args)
        else:
            print("Initial state is not solvable")
            print(unsolved_puzzle.formatted_puzzle)

    @staticmethod
    def __solve_core(unsolved_puzzle, args):
        puzzle_solution = Puzzle.generate_solution(unsolved_puzzle, args.final_state, args.blank_char)
        game = Game(unsolved_puzzle, puzzle_solution)
        result = game.run(args.algorithm, args.heuristic, args.metrics)
        if args.to_file:
            result[1].summary_to_file(args.to_file, args.show_path)
        else:
            result[1].summary_to_console(args.show_path)

    @staticmethod
    def __solve_batch(args):
        os.chdir(args.batch)
        files = glob.glob("*.puzzle")
        print_progress_bar(0, len(files), prefix='Progress:', suffix='Complete', length=50)
        for i, filename in enumerate(files):
            unsolved_puzzle = Puzzle.get_board_from_csv(UnsolvedPuzzle, filename, args.blank_char)
            if unsolved_puzzle.is_solvable(args.blank_char, args.final_state):
                Action.__solve_core(unsolved_puzzle, args)
            else:
                print("Initial state is not solvable")
            print_progress_bar(i+1, len(files), prefix='Progress:', suffix='Complete', length=50)


    @staticmethod
    def generate(args):
        def shuffle_puzzle(reference_puzzle: UnsolvedPuzzle):
            reference_puzzle_copy = copy.deepcopy(reference_puzzle)
            for _ in range(args.random_moves):
                reference_puzzle_copy.move(random.choice(reference_puzzle_copy.available_moves))
            return reference_puzzle_copy

        reference_puzzle = Puzzle.get_board_from_file(UnsolvedPuzzle, args.reference_file, args.blank_char)
        path = f'{args.destination}/puzzle{reference_puzzle.size ** 2 - 1}/moves_no_{args.random_moves}'
        for no in range(args.number):
            shuffled_puzzle = shuffle_puzzle(reference_puzzle)
            os.makedirs(path, exist_ok=True)
            with open(f'{path}/{no}-{id(shuffled_puzzle)}.puzzle', 'w') as f:
                f.write(shuffled_puzzle.csv_puzzle)
        with open(f'{path}/puzzle.solution', 'w') as f:
            f.write(reference_puzzle.csv_puzzle)
