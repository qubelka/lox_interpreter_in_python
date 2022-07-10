from lox import Lexer
from parser import Parser
from interpreter import Interpreter

while True:
    try:
        text = input("> ")
        if not text:
            continue
        lexer = Lexer("<stdin>", text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)
    except EOFError:
        break
    except Exception as e:
        print(e.as_string())
