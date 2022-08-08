from abc import ABCMeta, abstractmethod
from environment import Environment


class LoxCallable(metaclass=ABCMeta):
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter, arguments: list):
        pass


class LoxFunction(LoxCallable):
    def __init__(self, declaration):
        self.declaration = declaration

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter, arguments: list):
        environment = Environment(interpreter.environment)
        for i in range(len(self.declaration.params)):
            environment.define(
                self.declaration.params[i].value,
                arguments[i],
                self.declaration.params[i].pos_start,
                self.declaration.params[i].pos_end,
            )
        interpreter.execute_Block(self.declaration.body, environment)
        return None

    def __repr__(self):
        return f"<fn {self.declaration.name.value}>"
