from lox import (
    TT_BANG_EQUAL,
    TT_DIV,
    TT_EQ,
    TT_EQUAL_EQUAL,
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
    TT_STRING,
    TT_BANG,
    ErrorDetails,
)
from lox import InvalidSyntaxError


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


class Boolean(Factor):
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


class String(Factor):
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


class IfStmt(Stmt):
    def __init__(self, condition, then_stmt, else_stmt):
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

    def __repr__(self):
        return f"{self.condition}, {self.then_stmt}, {self.else_stmt}"


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.previous_token = self.current_token

    def eat(
        self,
        token_type,
        pos_start=None,
        pos_end=None,
        error=ErrorDetails.UNEXPECTED_TOKEN,
    ):
        if self.current_token.type == token_type:
            self.previous_token = self.current_token
            self.current_token = self.lexer.get_next_token()
        else:
            if not pos_start or not pos_end:
                pos_start = self.current_token.pos_start
                pos_end = self.current_token.pos_end
            raise InvalidSyntaxError(
                pos_start,
                pos_end,
                error,
            )

    def factor(self):
        token = self.current_token
        if token.type in (TT_MINUS, TT_BANG):
            if token.type == TT_MINUS:
                self.eat(TT_MINUS)
            else:
                self.eat(TT_BANG)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TT_NUMBER:
            self.eat(TT_NUMBER)
            return Num(token)
        elif token.type == TT_STRING:
            self.eat(TT_STRING)
            return String(token)
        elif token.type == TT_LPAREN:
            self.eat(TT_LPAREN)
            node = self.expression()
            if self.current_token.type == TT_RPAREN:
                self.eat(TT_RPAREN)
                return node
            else:
                raise InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    ErrorDetails.EXPECTED_RPAREN,
                )
        elif token.type == TT_IDENTIFIER:
            self.eat(TT_IDENTIFIER)
            return Identifier(token)
        elif token.matches(TT_KEYWORD, "nil"):
            self.eat(TT_KEYWORD)
            return Nil(token)
        elif token.matches(TT_KEYWORD, "true") or token.matches(TT_KEYWORD, "false"):
            self.eat(TT_KEYWORD)
            return Boolean(token)
        else:
            raise InvalidSyntaxError(
                self.current_token.pos_start,
                self.current_token.pos_end,
                ErrorDetails.EXPECTED_NUMBER,
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

    def comparison(self):
        return self.expr()

    def equality(self):
        node = self.comparison()
        while self.current_token.type in (TT_EQUAL_EQUAL, TT_BANG_EQUAL):
            operator = self.current_token
            if operator.type == TT_EQUAL_EQUAL:
                self.eat(TT_EQUAL_EQUAL)
            elif operator.type == TT_BANG_EQUAL:
                self.eat(TT_BANG_EQUAL)

            right = self.comparison()
            node = BinOp(node, operator, right)
        return node

    def block(self):
        self.eat(TT_LBRACE)
        statements = []
        while self.current_token.type not in (TT_RBRACE, TT_EOF):
            node = self.declaration()
            statements.append(node)
        self.eat(TT_RBRACE, ErrorDetails.EXPECTED_RBRACE)
        return statements

    def expression(self):
        return self.equality()

    def assignment(self):
        expr = self.expression()
        if self.current_token.type == TT_EQ:
            op = self.current_token
            self.eat(TT_EQ)
            value = self.assignment()
            if expr.token.type == TT_IDENTIFIER:
                return Assign(expr, op, value)
            raise InvalidSyntaxError(
                op.pos_start, op.pos_end, ErrorDetails.INVALID_ASSIGNMENT_TARGET
            )
        return expr

    def if_stmt(self):
        self.eat(TT_LPAREN)
        condition = self.expression()
        self.eat(TT_RPAREN)
        then_stmt = self.statement()
        else_stmt = None
        if self.current_token.matches(TT_KEYWORD, "else"):
            self.eat(TT_KEYWORD)
            else_stmt = self.statement()
        return IfStmt(condition, then_stmt, else_stmt)

    def print_stmt(self):
        expr = self.expression()
        self.eat(
            TT_SEMI,
            self.current_token.pos_start,
            self.current_token.pos_end,
            ErrorDetails.EXPECTED_SEMICOLON_AFTER_EXPRESSION,
        )
        return PrintStmt(expr)

    def expression_stmt(self):
        expr = self.assignment()
        self.eat(
            TT_SEMI,
            self.current_token.pos_start,
            self.current_token.pos_end,
            ErrorDetails.EXPECTED_SEMICOLON_AFTER_EXPRESSION,
        )
        return expr

    def statement(self):
        if self.current_token.matches(TT_KEYWORD, "print"):
            self.eat(TT_KEYWORD)
            return self.print_stmt()
        elif self.current_token.type == TT_LBRACE:
            return Block(self.block())
        elif self.current_token.matches(TT_KEYWORD, "if"):
            self.eat(TT_KEYWORD)
            return self.if_stmt()
        return self.expression_stmt()

    def var_decl(self):
        token = self.current_token
        self.eat(TT_IDENTIFIER, ErrorDetails.EXPRECTED_VARIABLE_NAME)
        expr = None
        if self.current_token.type == TT_EQ:
            self.eat(TT_EQ)
            expr = self.expression()
        self.eat(
            TT_SEMI,
            self.previous_token.pos_start,
            self.previous_token.pos_end,
            ErrorDetails.EXPECTED_SEMICOLON_AFTER_EXPRESSION,
        )
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
                ErrorDetails.EXPECTED_ARITHMETIC_OPERATOR,
            )
        return node
