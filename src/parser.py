from lox import TT_DIV, TT_MINUS, TT_MUL, TT_NUMBER, TT_PLUS, TT_LPAREN, TT_RPAREN
from lox import IllegalCharError, InvalidSyntaxError

class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self):
        return f'({self.left}, {self.op}, {self.right})'
    
class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f'{self.token}'
    

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            previous_token = self.lexer.text[self.lexer.previous_pos.idx]
            raise InvalidSyntaxError(self.lexer.previous_pos, self.current_token.pos_start, "'"+previous_token+"'")
    
    def factor(self):
        token = self.current_token
        if token.type == TT_NUMBER:
            self.eat(TT_NUMBER)
            return Num(token)
        elif token.type == TT_LPAREN:
            self.eat(TT_LPAREN)
            node = self.expr()
            self.eat(TT_RPAREN)
            return node
        else:
            previous_token = self.lexer.text[self.lexer.previous_pos.idx]
            raise InvalidSyntaxError(self.lexer.previous_pos, self.current_token.pos_start, "'"+previous_token+"'")
    
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
    
    def parse(self):
        return self.expr()
