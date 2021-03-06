import csv
import itertools
from math import sqrt

from src.solver.direction import Direction
from src.solver.state_generator import StateGenerator


class State:
    def __init__(self, state, size, cost=None, parent=None):
        self.state = state
        self.size: int = size
        self.parent = parent
        self.cost = cost
        self.cost_function = lambda x: 1

    def __hash__(self):
        return hash(self.state)

    def __lt__(self, other):
        return self.cost_function(self) < self.cost_function(other)

    def __le__(self, other):
        return self.cost_function(self) <= self.cost_function(other)


class Puzzle(State):
    @classmethod
    def __get_final_states(cls):
        final_states = {
            'blank_first': StateGenerator.generate_blank_first_state,
            'blank_last': StateGenerator.generate_blank_last_state
        }
        return final_states

    def __init__(self, board, blank, blank_char):
        super().__init__(tuple(itertools.chain.from_iterable(board)), len(board))
        self.board: list = board
        self.blank: tuple = blank
        self.blank_char: str = blank_char

    @staticmethod
    def get_board_from_csv(puzzle_class, path, blank_char):
        with open(path) as f:
            board = list(csv.reader(f))
            Puzzle.validate_puzzle(board, path)
            blank = Puzzle.find_blank(board, blank_char)
        return puzzle_class(board, blank, blank_char)

    @staticmethod
    def get_board_from_file(puzzle_class, f, blank_char):
        board = list(csv.reader(f))
        Puzzle.validate_puzzle(board, f)
        blank = Puzzle.find_blank(board, blank_char)
        return puzzle_class(board, blank, blank_char)

    @staticmethod
    def get_board_flat(puzzle_class, state, blank_char):
        board = []
        size = int(sqrt(len(state)))
        for x in range(size):
            board.append(state[x * size:size + x * size])
        Puzzle.validate_puzzle(board)
        blank = Puzzle.find_blank(board, blank_char)
        return puzzle_class(board, blank, blank_char)

    @staticmethod
    def generate_solution(init_state, final_state, blank_char):
        # noinspection PyArgumentList
        return Puzzle.__get_final_states()[final_state](blank_char, init_state.size)

    @classmethod
    def possible_final_states(cls):
        return Puzzle.__get_final_states().keys()

    @staticmethod
    def find_blank(board, blank_char):
        for i, sub_list in enumerate(board):
            if blank_char in sub_list:
                return i, sub_list.index(blank_char)

    @staticmethod
    def validate_puzzle(board, path='memory'):
        if not board:
            raise Exception(f"Board must not be empty <{path}>")
        if not all([len(i) == len(board) for i in board]):
            raise Exception(f"Board is not square {board} in file '{path}'")
        if len(list(itertools.chain.from_iterable(board))) != len(set(itertools.chain.from_iterable(board))):
            raise Exception(f"Elements in Board have to be unique {board} in file '{path}'")

    def is_solvable(self, blank_char, final_state):
        state = self.state
        if final_state == 'blank_last':
            state = list(reversed(state))
        inversions_no = self.find_inversions(blank_char, state)
        if inversions_no % 2 == 0 and self.size % 2 == 1:
            return True
        if self.size % 2 == 0:
            if (self.size - state.index(blank_char) // self.size) % 2 == 0 and inversions_no % 2 == 0:
                return True
            if (self.size - state.index(blank_char) // self.size) % 2 == 1 and inversions_no % 2 == 1:
                return True
        return False

    @staticmethod
    def find_inversions(blank_char, state):
        int_state = [int(x) for x in state if x != blank_char]
        n = len(int_state)
        inv_count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if int_state[i] > int_state[j]:
                    inv_count += 1
        return inv_count

    @property
    def formatted_puzzle(self):
        row_formatted = ["\t|\t".join(x) for x in self.board]
        board_formatted = ("\n" + ("-\t" * (2 * self.size - 1) + "\n")).join(row_formatted)
        return board_formatted

    @property
    def csv_puzzle(self):
        row_formatted = [",".join(x) for x in self.board]
        csv_puzzle = "\n".join(row_formatted)
        return csv_puzzle

    def puzzle_field(self, coords):
        return self.board[coords[0]][coords[1]]


class PuzzleSolution(Puzzle):
    pass


class UnsolvedPuzzle(Puzzle):
    def move(self, direction):
        if direction not in self.available_moves:
            raise Exception("Direction is not available")
        if direction is Direction.UP:
            new_blank = (self.blank[0] - 1, self.blank[1])
        elif direction is Direction.RIGHT:
            new_blank = (self.blank[0], self.blank[1] + 1)
        elif direction is Direction.DOWN:
            new_blank = (self.blank[0] + 1, self.blank[1])
        elif direction is Direction.LEFT:
            new_blank = (self.blank[0], self.blank[1] - 1)
        else:
            raise Exception("Wrong Direction")
        self.board[self.blank[0]][self.blank[1]] = self.puzzle_field(new_blank)
        self.board[new_blank[0]][new_blank[1]] = self.blank_char
        self.blank = new_blank

    @property
    def available_moves(self):
        moves = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        if self.blank[0] == 0:
            moves.remove(Direction.UP)
        if self.blank[1] == len(self.board) - 1:
            moves.remove(Direction.RIGHT)
        if self.blank[0] == len(self.board) - 1:
            moves.remove(Direction.DOWN)
        if self.blank[1] == 0:
            moves.remove(Direction.LEFT)
        return moves
