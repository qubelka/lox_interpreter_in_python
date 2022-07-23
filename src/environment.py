from lox import RTError


class Environment:
    def __init__(self, enclosing=None):
        self.values = dict()
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def assign(self, name, value, pos_start, pos_end):
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value, pos_start, pos_end)
            return
        raise RTError(pos_start, pos_end, f"Undefined variable '{name}'")

    def get(self, pos_start, pos_end, name):
        if self.values.get(name) is not None:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(pos_start, pos_end, name)
        raise RTError(pos_start, pos_end, f"Undefined variable '{name}'")

    def __repr__(self):
        return str(self.values)
