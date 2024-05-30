# N Puzzle Problem Solver

This project is a Python implementation of the N Puzzle Problem Solver. The N Puzzle Problem is a sliding puzzle that consists of a frame of numbered square tiles in random order with one tile missing. The object of the puzzle is to place the tiles in order by making sliding moves that use the empty space.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development purposes.

### Prerequisites

What things you need to install the software and how to install them:

```
Python 3.x
```

### Installing

A step by step series of examples that tell you how to get a development environment running:

```
git clone <repository_url>
cd <repository_name>
```

This project does not require any additional dependencies.

## Usage

`python main.py generate --help` will show you the help message for the generate command.

`python main.py solve --help` will show you the help message for the solve command.


Here are some examples of how to use this project from the command line:

### Generate a random puzzle


#### Generate a random puzzle with 8 tiles
```
python main.py generate -R 100 -n 8 -r samples/sample8/initial.csv
```

This will generate a random puzzle with 8 tiles and one blank tile based on `samples/sample8/initial.csv`. 

With 100 random moves, the puzzle will be generated and saved default location `generated/puzzle8/moves_no_100`.


#### Generate a random puzzle with 15 tiles
```
python main.py generate -R 200 -n 15 -r samples/sample15/initial.csv -d .
```
With 200 random moves, the puzzle will be generated and saved default location `./puzzle15/moves_no_200`.

### Solve a puzzle

#### Solve a puzzle with 8 tiles
```
python main.py solve -i samples/sample8/initial.csv  -H manhattan  -a rta -f blank_last 
```

#### Solve already solved puzzle with 8 tiles
```
python main.py solve -i samples/sample8/result.csv  -H manhattan  -a rta -f blank_first 
```

#### Solve batch of puzzles with 8 tiles

Previously generated puzzles can be solved in batch mode. 

```
python main.py solve  -H manhattan  -a rta -f blank_last --metrics --batch generated/puzzle8/moves_no_10
```
