# Puzzlr

Puzzlr is a team based game for making and solving numerical puzzles.

Two teams battle it out to make the best defence while trying to
sabotage the other team.

You create defences using puzzle objects. A puzzle object is an object
with 5 integers in it as state, and operations defined on the puzzle. The
success state of the puzzle has all 0s.

You can costruct a puzzle using a `PuzzleFactory` object. first, create
the factory and call `add_operation(operation, name, inverse_name` on
the factory, then puzzle.bulid() to make the puzzle. The operation
object defines what is done to the state, the name is the name of the operation
, and the inverse will always be added and as of such the second name is the
inverse.

There is an example in Example.py

to create a puzzle, create a python file with the package function in it.
Then, return your puzzle object with the package. To serialise the puzzle
into a file, call:

```bash
python cli.py package puzzleDefinition.py myPuzzle.puzzle
```

This creates a file called myPuzzle.puzzle that you can send to your friends
to solve.

To solve a puzzle, create a python file with a solve function in the puzzle
which take a puzzle argument. Then call operations on the puzzle and return
the new puzzle.

Then, call:

```bash
python cli.py solve solver.py myPuzle.puzzle
```

And you're done! You can check out what operations are defined at the top
of Puzzlr.py and play around with this
