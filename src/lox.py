from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


class Lox:
    def __init__(self):
        self.interpreter = Interpreter()

    def run(self, text):
        lexer = Lexer("<stdin>", text)
        parser = Parser(lexer)
        return self.interpreter.interpret(parser)
