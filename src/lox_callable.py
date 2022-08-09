import time
from typing import TYPE_CHECKING, Any
from abc import ABCMeta, abstractmethod
from environment import Environment
from parser import Stmt

if TYPE_CHECKING:
    from interpreter import Interpreter


class LoxCallable(metaclass=ABCMeta):
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter: "Interpreter", arguments: list) -> Any:
        pass


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Stmt) -> None:
        self.declaration = declaration

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter: "Interpreter", arguments: list) -> Any:
        environment = Environment(interpreter.globals)
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


class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter: "Interpreter", arguments: list) -> Any:
        return time.time()

    def __repr__(self):
        return f"<native fn>"
