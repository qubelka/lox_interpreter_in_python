from lox import (
    TT_DIV,
    TT_EQ,
    TT_KEYWORD,
    TT_LBRACE,
    TT_MINUS,
    TT_MUL,
    TT_NUMBER,
    TT_PLUS,
    TT_LPAREN,
    TT_RBRACE,
    TT_RPAREN,
    TT_EOF,
    TT_SEMI,
    TT_IDENTIFIER,
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


class Factor(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"{self.token}"

class Nil(Factor):
    def __init__(self, token):
        super().__init__(token)
        

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self):
        return f"{self.left}, {self.op}, {self.right}"


class Num(Factor):
    def __init__(self, token):
        super().__init__(token)

class Identifier(Factor):
    def __init__(self, token):
        super().__init__(token)


class Stmt(object):
    pass


class PrintStmt(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"{self.expr}"


class VarStmt(Stmt):
    def __init__(self, token, expr):
        self.token = token
        self.expr = expr

    def __repr__(self):
        return f"{self.token}, {self.expr}"

class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type, error="Unexpected token"):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise InvalidSyntaxError(
                self.current_token.pos_start,
                self.current_token.pos_end,
                error,
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
        elif token.type == TT_IDENTIFIER:
            self.eat(TT_IDENTIFIER)
            return Identifier(token)
        elif token.matches(TT_KEYWORD, "nil"):
            self.eat(TT_KEYWORD)
            return Nil(token)
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

    def block(self):
        self.eat(TT_LBRACE)
        statements = []
        while self.current_token.type not in (TT_RBRACE, TT_EOF):
            node = self.declaration()
            statements.append(node)
        self.eat(TT_RBRACE, "Expected '}'")
        return statements

    def assignment(self):
        expr = self.expr()
        if (self.current_token.type == TT_EQ):
            op = self.current_token
            self.eat(TT_EQ)
            value = self.assignment()
            if expr.token.type == TT_IDENTIFIER:
                return Assign(expr, op, value)
            raise InvalidSyntaxError(op.pos_start, op.pos_end, "Invalid assignment target")
        self.eat(TT_SEMI, "Expected ';' after expression.")
        return expr

    def statement(self):
        if self.current_token.matches(TT_KEYWORD, "print"):
            self.eat(TT_KEYWORD)
            expr = self.assignment()
            return PrintStmt(expr)
        elif self.current_token.type == TT_LBRACE:
            return Block(self.block())
        node = self.assignment()
        return node

    def var_decl(self):
        token = self.current_token
        self.eat(TT_IDENTIFIER, "Expected variable name.")
        expr = None
        if self.current_token.type == TT_EQ:
            self.eat(TT_EQ)
            expr = self.expr()
        self.eat(TT_SEMI, "Expected ';' after expression.")
        return VarStmt(token, expr)

    def declaration(self):
        if self.current_token.matches(TT_KEYWORD, "var"):
            self.eat(TT_KEYWORD)
            return self.var_decl()
        else:
            return self.statement()

    def program(self):
        declarations = []
        while self.current_token.type != TT_EOF:
            declaration = self.declaration()
            declarations.append(declaration)
        return declarations

    def parse(self):
        node = self.program()
        if self.current_token.type != TT_EOF:
            raise InvalidSyntaxError(
                self.current_token.pos_start,
                self.current_token.pos_end,
                "Expected '+', '-', '*' or '/'",
            )
        return node
