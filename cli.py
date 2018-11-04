import sys
import importlib
import pickle
import os
from Puzzlr import serialise_puzzle, deserialise_puzzle

def main():
    if sys.argv[1] == 'package':
        puzzle = importlib.import_module(os.path.splitext(sys.argv[2])[0]).package()
        with open(sys.argv[3], 'wb') as f:
            pickle.dump(serialise_puzzle(puzzle), f)
    elif sys.argv[1] == 'solve':
        with open(sys.argv[3], 'rb') as f:
            puzzle = deserialise_puzzle(pickle.load(f))
            end = importlib.import_module(os.path.splitext(sys.argv[2])[0]).solve(puzzle)
            for i in range(len(end.state)):
                if end.state[i] != 0:
                    print("Failure")
                    return
            print("Success!!!!!")

main()
