from environment import Environment
from lox import (
    TT_PLUS,
    TT_MINUS,
    TT_MUL,
    TT_DIV,
    ErrorDetails
)

from lox import RTError


class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")


class Interpreter(NodeVisitor):
    def __init__(self, parser, environment):
        self.parser = parser
        self.environment = environment

    def is_truthy(self, value):
        if value == None or value == "nil" or value == "false":
            return False
        return True

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        pos_start = node.token.pos_start
        pos_end = node.token.pos_end

        if not isinstance(left, float) or not isinstance(right, float):
            raise RTError(pos_start, pos_end, ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS)

        if node.op.type == TT_PLUS:
            return left + right
        elif node.op.type == TT_MINUS:
            return left - right
        elif node.op.type == TT_MUL:
            return left * right
        elif node.op.type == TT_DIV:
            if right == 0:
                raise RTError(pos_start, pos_end, ErrorDetails.DIVISION_BY_ZERO)
            else:
                return left / right

    def visit_Num(self, node):
        return node.value
    
    def visit_String(self, node):
        return node.value

    def visit_Nil(self, node):
        return node.value

    def visit_Boolean(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == TT_MINUS:
            expr = node.expr
            result = self.visit(expr)
            if not isinstance(result, float):
                raise RTError(expr.token.pos_start, expr.token.pos_end, ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS)
            return -result

    def visit_PrintStmt(self, node):
        result = self.visit(node.expr)
        print(result)
        return None

    def visit_VarStmt(self, stmt):
        value = "nil"
        if stmt.expr:
            value = self.visit(stmt.expr)
        self.environment.define(stmt.token.value, value)
        return None

    def visit_IfStmt(self, node):
        condition = self.visit(node.condition)
        if self.is_truthy(condition):
            self.visit(node.then_stmt)
        elif node.else_stmt is not None:
          self.visit(node.else_stmt)
        return None

    def visit_Block(self, node):
        previous_env = self.environment
        self.environment = Environment(previous_env)
        for stmt in node.statements:
            self.visit(stmt)
        self.environment = previous_env

    def visit_Assign(self, node):
        var_name = node.left.value
        value = self.visit(node.right)
        self.environment.assign(var_name, value, node.left.token.pos_start, node.left.token.pos_end)
        return value

    def visit_Identifier(self, node):
        return self.environment.get(node.token.pos_start, node.token.pos_end, node.value)

    def interpret(self):
        tree = self.parser.parse()
        if not tree:
            return None
        for node in tree:
            result = self.visit(node)
        return result
