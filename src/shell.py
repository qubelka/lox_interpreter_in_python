import sys
from lox import Lexer
from parser import Parser
from interpreter import Interpreter
from environment import Environment

environment = Environment()

while True:
    try:
        repl = True
        text = None
        if len(sys.argv) > 1:
            repl = False
            text = open(sys.argv[1], 'r').read()
        else:
            text = input("> ")
        if not text:
            continue
        lexer = Lexer("<stdin>", text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser, environment)
        result = interpreter.interpret()
        if not repl:
            break
        if result is not None:
            print(result)

    except EOFError:
        break
    except Exception as e:
        print(e.as_string())
        if not repl:
            break
