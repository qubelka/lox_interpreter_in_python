from enum import Enum
import string

DIGITS = "1234567890"
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

# Token types
TT_NUMBER = "NUMBER"
TT_STRING = "STRING"
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
TT_BANG_EQUAL = "BANG_EQUAL"
TT_BANG = "BANG"
TT_LESS_EQUAL = "LESS_EQUAL"
TT_LESS = "LESS"
TT_GREATER_EQUAL = "GREATER_EQUAL"
TT_GREATER = "GREATER"
TT_EQUAL_EQUAL = "EQUAL_EQUAL"
TT_COMMA = "COMMA"

KEYWORDS = {
    "print": True,
    "var": True,
    "nil": True,
    "true": True,
    "false": True,
    "if": True,
    "else": True,
    "and": True,
    "or": True,
    "while": True,
    "for": True,
    "fun": True,
    "return": True
}


class ErrorDetails(Enum):
    DIVISION_BY_ZERO = "Division by zero"
    CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS = (
        "Can apply arithmetic operations only to numbers"
    )
    UNTERMINATED_STRING = "Unterminated string"
    UNEXPECTED_TOKEN = "Unexpected token"
    INVALID_ASSIGNMENT_TARGET = "Invalid assignment target"
    EXPECTED_SEMICOLON_AFTER_EXPRESSION = "Expected ';' after expression"
    EXPRECTED_VARIABLE_NAME = "Expected variable name"
    EXPECTED_NUMBER = "Expected number"
    EXPECTED_LPAREN = "Expected '('"
    EXPECTED_RPAREN = "Expected ')'"
    EXPECTED_RBRACE = "Expected '}'"
    EXPECTED_ARITHMETIC_OPERATOR = "Expected '+', '-', '*' or '/'"
    TRAILING_DOT = "Trailing dot"
    LEADING_DOT = "Leading dot"
    TOO_MANY_DOTS = "Too many dots"
    UNDEFINED_VARIABLE = "Undefined variable"
    BINARY_OPS_TYPE_ERROR = "Can apply binary operations only to numbers, strings or booleans.\nThe operands must be of the same type."
    CALLS_RESTRICTION = "Can only call functions and classes"
    CANT_HAVE_MORE_THAN_255_ARGS = "Can't have more than 255 arguments"
    EXPECTED_FUNCTION_NAME =  "Expected function name"
    EXPECTED_PARAMETER_NAME = "Expected parameter name"
    EXPECTED_SEMICOLON = "Expected ';'"


class Error(Exception):
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        input_as_rows = self.pos_start.ftxt.split("\n")
        row_with_error = input_as_rows[self.pos_start.ln]
        error_prefix = f"   {self.pos_start.ln+1} | "
        result = f"{self.error_name}: {self.details.value if isinstance(self.details, ErrorDetails) else self.details}\n\n"
        result += f"{error_prefix}{row_with_error}\n"
        result += " " * len(error_prefix) + " " * self.pos_start.row_length + "^"
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


class Return(Exception):
    def __init__(self, value):
        self.value = value


class Position:
    def __init__(self, idx, ln, col, fn, ftxt, row_length):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
        self.row_length = row_length

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1
        self.row_length += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0
            self.row_length = 0

        return self

    def copy(self):
        return Position(
            self.idx, self.ln, self.col, self.fn, self.ftxt, self.row_length
        )


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
        if self.value is not None:
            return f"{self.type}:{self.value}"
        return f"{self.type}"


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(0, 0, 0, fn, text, 0)
        self.current_char = self.text[self.pos.idx]

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        )

    def peek(self):
        return (
            self.text[self.pos.idx + 1] if self.pos.idx + 1 < len(self.text) else None
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
                if self.peek() == "/":
                    while self.current_char not in ["\n", None]:
                        self.advance()
                    continue
                else:
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
                if self.peek() == "=":
                    self.advance()
                    token = Token(TT_EQUAL_EQUAL, "==", self.pos)
                self.advance()
                return token

            if self.current_char == "!":
                token = Token(TT_BANG, "!", self.pos)
                if self.peek() == "=":
                    self.advance()
                    token = Token(TT_BANG_EQUAL, "!=", self.pos)
                self.advance()
                return token

            if self.current_char == "<":
                token = Token(TT_LESS, "<", self.pos)
                if self.peek() == "=":
                    self.advance()
                    token = Token(TT_LESS_EQUAL, "<=", self.pos)
                self.advance()
                return token

            if self.current_char == ">":
                token = Token(TT_GREATER, ">", self.pos)
                if self.peek() == "=":
                    self.advance()
                    token = Token(TT_GREATER_EQUAL, ">=", self.pos)
                self.advance()
                return token

            if self.current_char == '"':
                self.advance()
                return self.make_string()

            if self.current_char == ",":
                self.advance()
                return Token(TT_COMMA, ",", self.pos)

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
                    return None, InvalidSyntaxError(
                        pos_start, self.pos, ErrorDetails.TOO_MANY_DOTS
                    )
                elif len(num_str) == 0:
                    # error: leading dot
                    pos_start = self.pos.copy()
                    self.advance()
                    return None, InvalidSyntaxError(
                        pos_start, self.pos, ErrorDetails.LEADING_DOT
                    )
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
            return None, InvalidSyntaxError(
                pos_start, self.pos, ErrorDetails.TRAILING_DOT
            )
        return Token(TT_NUMBER, float(num_str), pos_start, self.pos), None

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + "_":
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if KEYWORDS.get(id_str) else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_string(self):
        pos_start = self.pos.copy()
        while self.current_char not in ['"', None]:
            self.advance()

        if self.current_char is None:
            pos_start = self.pos.copy()
            raise InvalidSyntaxError(
                pos_start, self.pos, ErrorDetails.UNTERMINATED_STRING
            )

        self.advance()
        return Token(
            TT_STRING, self.text[pos_start.idx : self.pos.idx - 1], pos_start, self.pos
        )
