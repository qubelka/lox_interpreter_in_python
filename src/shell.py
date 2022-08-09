import sys
from lox import Lox


lox = Lox()

while True:
    try:
        repl = True
        text = None
        if len(sys.argv) > 1:
            repl = False
            text = open(sys.argv[1], "r").read()
        else:
            text = input("> ")
        if not text:
            continue
        result = lox.run(text)
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
