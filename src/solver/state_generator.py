


class StateGenerator:
    @classmethod
    def generate_blank_first_state(cls, blank_char, size):
        from src.solver.board import Puzzle, PuzzleSolution
        flat_board = [blank_char] + [str(x) for x in range(1, size**2)]
        return Puzzle.get_board_flat(PuzzleSolution, flat_board, blank_char)

    @classmethod
    def generate_blank_last_state(cls, blank_char, size):
        from src.solver.board import Puzzle, PuzzleSolution
        flat_board = [str(x) for x in range(1, size ** 2)] + [blank_char]
        return Puzzle.get_board_flat(PuzzleSolution, flat_board, blank_char)
