from lox import (
    TT_DIV,
    TT_KEYWORD,
    TT_MINUS,
    TT_MUL,
    TT_NUMBER,
    TT_PLUS,
    TT_LPAREN,
    TT_RPAREN,
    TT_EOF,
    TT_SEMI,
)
from lox import IllegalCharError, InvalidSyntaxError


class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self):
        return f"({self.left}, {self.op}, {self.right})"


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __repr__(self):
        return f"{self.token}, {self.expr}"


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"{self.token}"


class Stmt(object):
    pass


class Print(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"{self.expr}"


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise InvalidSyntaxError(
                self.current_token.pos_start,
                self.current_token.pos_end,
                "Unexpected token",
            )

    def factor(self):
        token = self.current_token
        if token.type == TT_MINUS:
            self.eat(TT_MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TT_NUMBER:
            self.eat(TT_NUMBER)
            return Num(token)
        elif token.type == TT_LPAREN:
            self.eat(TT_LPAREN)
            node = self.expr()
            if self.current_token.type == TT_RPAREN:
                self.eat(TT_RPAREN)
                return node
            else:
                raise InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected ')'",
                )
        else:
            raise InvalidSyntaxError(
                self.current_token.pos_start,
                self.current_token.pos_end,
                "Expected number",
            )

    def term(self):
        node = self.factor()

        while self.current_token.type in (TT_MUL, TT_DIV):
            token = self.current_token
            if token.type == TT_MUL:
                self.eat(TT_MUL)
            elif token.type == TT_DIV:
                self.eat(TT_DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (TT_PLUS, TT_MINUS):
            token = self.current_token
            if token.type == TT_PLUS:
                self.eat(TT_PLUS)
            elif token.type == TT_MINUS:
                self.eat(TT_MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def statement(self):
        if self.current_token.matches(TT_KEYWORD, "print"):
            self.eat(TT_KEYWORD)
            node = self.expr()
            if self.current_token.type == TT_SEMI:
                self.eat(TT_SEMI)
                return Print(expr=node)
            else:
                raise InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected ';' after value.",
                )
        node = self.expr()
        return node

    def parse(self):
        node = self.statement()
        if self.current_token.type != TT_EOF:
            raise InvalidSyntaxError(
                self.current_token.pos_start,
                self.current_token.pos_end,
                "Expected '+', '-', '*' or '/'",
            )
        return node
