import importlib
import sys
import pickle
import types

class SwapOperation:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def apply(self, state):
        state[self.p1], state[self.p2] = state[self.p2], state[self.p1]
        return state

    def reverse(self, state):
        state[self.p1], state[self.p2] = state[self.p2], state[self.p1]
        return state

    def serialise(self):
        return {
            'name': "SwapOperation",
            'args': [self.p1, self.p2]
        }

class CompoundOperation:
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2

    def apply(self, state):
        return self.op2.apply(self.op1.apply(state))

    def reverse(self, state):
        return self.op2.reverse(self.op1.reverse(state))

    def serialise(self):
        return {
            'name': 'CompoundOperation',
            'args': [self.op1.serialise(), self.op2.serialise()],
        }


class AddOperation:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def apply(self, state):
        state[self.p1] += state[self.p2]
        return state

    def reverse(self, state):
        state[self.p1] -= state[self.p2]
        return state

    def serialise(self):
        return {
            'name': "AddOperation",
            'args': [self.p1, self.p2]
        }


class SubOperation:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def apply(self, state):
        state[self.p1] -= state[self.p2]
        return state

    def reverse(self, state):
        state[self.p1] += state[self.p2]
        return state

    def serialise(self):
        return {
            'name': "SubOperation",
            'args': [self.p1, self.p2]
        }


class AddConstOperation:
    def __init__(self, index, by):
        self.index = index
        self.by = by

    def apply(self, state):
        state[self.index] += self.by
        return state

    def reverse(self, state):
        state[self.index] -= self.by
        return state

    def serialise(self):
        return {
            'name': "AddConstOperation",
            'args': [self.index, self.by]
        }

class SubConstOperation:
    def __init__(self, index, by):
        self.index = index
        self.by = by

    def apply(self, state):
        state[self.index] -= self.by
        return state

    def reverse(self, state):
        state[self.index] += self.by
        return state

    def serialise(self):
        return {
            'name': "SubConstOperation",
            'args': [self.index, self.by]
        }

def serialise_puzzle(puzzle):
    obj = {
        'state': puzzle.state,
        'operations': []
    }
    for key in dir(puzzle):
        if not key.startswith("_") and callable(getattr(puzzle, key)):
            function = getattr(puzzle, key)
            if function._direction == "op":
                obj['operations'].append({
                    'operator': function._operator.serialise(),
                    'names': [key, function._invname]
                })

    return obj

def add_single_operation(puzzle, operation, name, direction):
    def op(self):
        if direction == "op":
            self.state = operation.apply(self.state)
        elif direction == "invop":
            self.state = operation.reverse(self.state)


    op.__name__ = name
    op._operator = operation
    op._direction = direction

    setattr(puzzle, name, types.MethodType(op, self.puzzle))

def deserialise_operation(given_operation):
    operations = [
        SwapOperation,
        AddOperation,
        SubOperation,
        AddConstOperation,
        SubConstOperation,
        CompoundOperation,
    ]
    args = given_operation['args']
    if given_operation['name'] == "CompoundOperation":
        args = [deserialise_operation(x) for x in args]

    for operation in operations:
        if operation.__name__ == given_operation['name']:
            return operation(*args)


def deserialise_puzzle(obj):
    operations = [
        SwapOperation,
        AddOperation,
        SubOperation,
        AddConstOperation,
        SubConstOperation,
        CompoundOperation,
    ]

    factory = PuzzleFactory()
    for included_operation in obj['operations']:
        for operation in operations:
            if operation.__name__ == included_operation['operator']['name']:
                factory.add_operation(deserialise_operation(included_operation['operator']), *included_operation['names'])

    puzzle = factory.build()
    puzzle.state = obj['state']
    return puzzle


class PuzzleFactory:
    def __init__(self):
        self.puzzle = Puzzle()
    
    def add_operation(self, operation, name, inv_name):

        def op(self):
            self.state = operation.apply(self.state)

        op.__name__ = name
        op._operator = operation
        op._direction = "op"
        op._invname = inv_name

        def invop(self):
            self.state = operation.reverse(self.state)

        invop.__name__ = inv_name
        invop._operator = operation
        invop._direction = "invop"

        setattr(self.puzzle, name, types.MethodType(op, self.puzzle))
        setattr(self.puzzle, inv_name, types.MethodType(invop, self.puzzle))

    def build(self):
        return self.puzzle


class Puzzle:
    def __init__(self):
        self.state = [0, 0, 0, 0, 0]

