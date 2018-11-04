from Puzzlr import *

def package():
    factory = PuzzleFactory()
    factory.add_operation(SwapOperation(2, 3), "cat", "time")
    factory.add_operation(AddConstOperation(2, 3), "down", "space")

    puzzle = factory.build()
    puzzle.down()
    puzzle.down()
    puzzle.cat()
    puzzle.down()
    return puzzle

def solve(puzzle):
    puzzle.space()
    puzzle.time()
    puzzle.space()
    puzzle.space()
    print(puzzle.state)
    return puzzle
