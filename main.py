from _ast import arg

from src.action import Action
from src.cli import parse_arguments

args = parse_arguments()
if args.action == 'solve':
    Action.solve(args)
elif args.action == 'generate':
    Action.generate(arg)

