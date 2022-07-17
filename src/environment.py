from lox import RTError


class Environment:
    def __init__(self):
        self.values = dict()

    def __setitem__(self, name, value):
        self.values[name] = value

    def get(self, pos_start, pos_end, name):
        if self.values.get(name) is not None:
            return self.values[name]
        print(self.values)
        raise RTError(pos_start, pos_end, f"Undefined variable '{name}'")

    def __repr__(self):
        return str(self.values)
