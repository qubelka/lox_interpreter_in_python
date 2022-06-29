from lox import Lexer
from parser import Parser

while True:
    try: 
        text = input('> ')
        if not text:
            continue
        lexer = Lexer('<stdin>', text)
        parser = Parser(lexer)
        result = parser.parse()
        print(result)
    except EOFError:
        break
    except Exception as e:
        print(e.as_string())