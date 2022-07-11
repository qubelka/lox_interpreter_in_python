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
        """
        REPL accepts statements or expressions:
        statement -> printStmt;
        printStmt -> "print" expression ";";
        expression -> term;
        """
        if result: 
            print(result)
    except EOFError:
        break
    except Exception as e:
        print(e.as_string())
