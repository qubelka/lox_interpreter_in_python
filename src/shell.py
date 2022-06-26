import lox

while True:
    text = input('> ')
    result, error = lox.run('<stdin>', text)

    if error: 
        print(error.as_string())
    else:
        print(result)