import csv

from src.direction import Direction


class Puzzle:
    def __init__(self, board, head, head_char):
        self.board: list = board
        self.head: tuple = head
        self.head_char: str = head_char

    @staticmethod
    def get_board_from_csv(puzzle_class, path, head_char):
        with open(path) as f:
            board = list(csv.reader(f))
            Puzzle.validate_puzzle(board)
            head = Puzzle.find_head(board, head_char)
        return puzzle_class(board, head, head_char)

    @staticmethod
    def find_head(board, character):
        for i, sub_list in enumerate(board):
            if character in sub_list:
                return i, sub_list.index(character)

    @staticmethod
    def validate_puzzle(board):
        if not board:
            raise Exception("Board must not be empty")
        if not all([len(i) == len(board) for i in board]):
            raise Exception(f"Board is not square <{board}>")

    @property
    def formatted_puzzle(self):
        row_formatted = ["\t|\t".join(x) for x in self.board]
        board_formatted = ("\n" + ("-\t" * (2 * len(self.board) - 1) + "\n")).join(row_formatted)
        return board_formatted

    def puzzle_field(self, coords):
        return self.board[coords[0]][coords[1]]


class PuzzleSolution(Puzzle):
    pass


class UnsolvedPuzzle(Puzzle):
    def move(self, direction):
        if direction not in self.available_moves:
            raise Exception("Direction is not available")
        if direction is Direction.UP:
            new_head = (self.head[0] - 1, self.head[1])
        elif direction is Direction.RIGHT:
            new_head = (self.head[0], self.head[1] + 1)
        elif direction is Direction.DOWN:
            new_head = (self.head[0] + 1, self.head[1])
        elif direction is Direction.LEFT:
            new_head = (self.head[0], self.head[1] - 1)
        else:
            raise Exception("Wrong Direction")
        self.board[self.head[0]][self.head[1]] = self.puzzle_field(new_head)
        self.board[new_head[0]][new_head[1]] = self.head_char
        self.head = new_head

    @property
    def available_moves(self):
        moves = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        if self.head[0] == 0:
            moves.remove(Direction.UP)
        if self.head[1] == len(self.board) - 1:
            moves.remove(Direction.RIGHT)
        if self.head[0] == len(self.board) - 1:
            moves.remove(Direction.DOWN)
        if self.head[1] == 0:
            moves.remove(Direction.LEFT)
        return moves