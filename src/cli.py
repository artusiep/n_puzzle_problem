import argparse


def parse_arguments():
    from src.solver.board import Puzzle
    from src.solver.heuristics import Heuristic

    parser = argparse.ArgumentParser(prog='N Puzzle Tool', description='N Puzzle Solver.')

    subparsers = parser.add_subparsers(help="Possible commands", dest='action')
    subparsers.required = True

    solve_parser = subparsers.add_parser("solve")
    generate_parser = subparsers.add_parser("generate")

    solve_parser.add_argument('-H', '--heuristic', choices=Heuristic.available_heuristic(), required=True)
    solve_parser.add_argument('-f', '--final_state', choices=Puzzle.possible_final_states(), required=True)
    solve_parser.add_argument('-b', '--blank_char', default='x')

    group = solve_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--init_file', type=argparse.FileType('r'))
    group.add_argument('--batch', type=str)

    generate_parser.add_argument('-n', '--number', type=int, required=True)
    generate_parser.add_argument('-d', '--destination', type=str, default='./generated')
    generate_parser.add_argument('-r', '--reference_file', type=argparse.FileType('r'), required=True)
    generate_parser.add_argument('-b', '--blank_char', default='x')

    args = parser.parse_args()
    return args
