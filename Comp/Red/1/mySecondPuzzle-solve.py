from Puzzlr import *

def solve(puzzle):
    print(puzzle.state)
    print(dir(puzzle))
    for i in range(4798):
        puzzle.tomate()
        puzzle.read()
    print(puzzle.state)
    print(dir(puzzle))
    return puzzle