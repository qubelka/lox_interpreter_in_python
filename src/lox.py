import string

DIGITS = "1234567890"
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

# Token types
TT_NUMBER = "NUMBER"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_EQ = "EQ"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LBRACE = "LBRACE"
TT_RBRACE = "RBRACE"
TT_EOF = "EOF"
TT_KEYWORD = "KEYWORD"
TT_SEMI = "SEMI"
TT_IDENTIFIER = "IDENTIFIER"

KEYWORDS = ["print", "var"]


class Error(Exception):
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        error_prefix = f"   {self.pos_start.ln+1} | "
        result = f"{self.error_name}: {self.details}\n\n"
        result += f"{error_prefix}{self.pos_start.ftxt}\n"
        result += " " * len(error_prefix) + " " * self.pos_start.idx + "^"
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal character", details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__(pos_start, pos_end, "Invalid syntax", details)


class RTError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Runtime Error", details)


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


class Token:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(0, 0, 0, fn, text)
        self.current_char = self.text[self.pos.idx]

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        )

    def get_next_token(self):
        while self.current_char != None:
            if self.current_char in " \t\n":
                self.advance()
                continue

            if self.current_char == "+":
                token = Token(TT_PLUS, "+", self.pos)
                self.advance()
                return token

            if self.current_char == "-":
                token = Token(TT_MINUS, "-", self.pos)
                self.advance()
                return token

            if self.current_char == "*":
                token = Token(TT_MUL, "*", self.pos)
                self.advance()
                return token

            if self.current_char == "/":
                token = Token(TT_DIV, "/", self.pos)
                self.advance()
                return token

            if self.current_char == "(":
                token = Token(TT_LPAREN, "(", self.pos)
                self.advance()
                return token

            if self.current_char == ")":
                token = Token(TT_RPAREN, ")", self.pos)
                self.advance()
                return token

            if self.current_char == "{":
                token = Token(TT_LBRACE, "{", self.pos)
                self.advance()
                return token

            if self.current_char == "}":
                token = Token(TT_RBRACE, "}", self.pos)
                self.advance()
                return token

            if self.current_char == ";":
                token = Token(TT_SEMI, ";", self.pos)
                self.advance()
                return token

            if self.current_char == "=":
                token = Token(TT_EQ, "=", self.pos)
                self.advance()
                return token

            if self.current_char in DIGITS:
                number_token, error = self.make_number()
                if error:
                    raise error
                return number_token

            if self.current_char in LETTERS:
                token = self.make_identifier()
                return token

            pos_start = self.pos.copy()
            invalid_char = self.current_char
            self.advance()
            raise IllegalCharError(pos_start, self.pos, "'" + invalid_char + "'")

        return Token(TT_EOF, pos_start=self.pos)

    def make_number(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    # error: too many dots
                    pos_start = self.pos.copy()
                    self.advance()
                    return None, InvalidSyntaxError(pos_start, self.pos)
                elif len(num_str) == 0:
                    # error: leading dot
                    pos_start = self.pos.copy()
                    self.advance()
                    return None, InvalidSyntaxError(pos_start, self.pos)
                else:
                    dot_count += 1
                    num_str += "."
            else:
                num_str += self.current_char
            self.advance()

        if num_str[-1] == ".":
            # error: trailing dot
            pos_start = self.pos.copy()
            self.advance()
            return None, InvalidSyntaxError(pos_start, self.pos)
        return Token(TT_NUMBER, float(num_str), pos_start, self.pos), None

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + "_":
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)
