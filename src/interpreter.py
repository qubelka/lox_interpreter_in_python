from environment import Environment
from lox import (
    TT_BANG,
    TT_BANG_EQUAL,
    TT_EQUAL_EQUAL,
    TT_KEYWORD,
    TT_LESS,
    TT_LESS_EQUAL,
    TT_PLUS,
    TT_MINUS,
    TT_MUL,
    TT_DIV,
    TT_GREATER,
    TT_GREATER_EQUAL,
    ErrorDetails,
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

    def check_types(self, pos_start, pos_end, v1, v2, equality_operation=False):
        allowed_types = ["nil", "false", "true"]

        if isinstance(v1, float):
            if isinstance(v2, float):
                return True
            if equality_operation and v2 in allowed_types:
                return True

        if isinstance(v2, float):
            if equality_operation and v1 in allowed_types:
                return True

        if isinstance(v1, str):
            if isinstance(v2, str):
                return True
            if equality_operation and v2 in allowed_types:
                return True

        if isinstance(v2, str):
            if equality_operation and v1 in allowed_types:
                return True

        if equality_operation and v1 in allowed_types and v2 in allowed_types:
            return True

        raise RTError(pos_start, pos_end, ErrorDetails.BINARY_OPS_TYPE_ERROR)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        pos_start = node.token.pos_start
        pos_end = node.token.pos_end

        if node.op.type == TT_PLUS:
            self.check_types(pos_start, pos_end, left, right)
            return left + right

        if node.op.type in (
            TT_MINUS,
            TT_MUL,
            TT_DIV,
            TT_GREATER,
            TT_GREATER_EQUAL,
            TT_LESS,
            TT_LESS_EQUAL,
        ):
            if not isinstance(left, float) or not isinstance(right, float):
                raise RTError(
                    pos_start,
                    pos_end,
                    ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
                )

            if node.op.type == TT_MINUS:
                return left - right
            elif node.op.type == TT_MUL:
                return left * right
            elif node.op.type == TT_DIV:
                if right == 0:
                    raise RTError(pos_start, pos_end, ErrorDetails.DIVISION_BY_ZERO)
                else:
                    return left / right
            elif node.op.type == TT_GREATER:
                return "true" if left > right else "false"
            elif node.op.type == TT_GREATER_EQUAL:
                return "true" if left >= right else "false"
            elif node.op.type == TT_LESS:
                return "true" if left < right else "false"
            elif node.op.type == TT_LESS_EQUAL:
                return "true" if left <= right else "false"

        self.check_types(pos_start, pos_end, left, right, True)

        if node.op.type == TT_EQUAL_EQUAL:
            return "true" if left == right else "false"
        if node.op.type == TT_BANG_EQUAL:
            return "true" if left != right else "false"

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
        expr = node.expr
        result = self.visit(expr)
        if op == TT_MINUS:
            if not isinstance(result, float):
                raise RTError(
                    expr.token.pos_start,
                    expr.token.pos_end,
                    ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
                )
            return -result
        if op == TT_BANG:
            return "true" if not self.is_truthy(result) else "false"

    def visit_Logical(self, node):
        left = self.visit(node.left)
        if node.op.matches(TT_KEYWORD, "or"):
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.visit(node.right)

    def visit_PrintStmt(self, node):
        result = self.visit(node.expr)
        print(result)
        return None

    def visit_VarStmt(self, stmt):
        value = "nil"
        if stmt.expr:
            value = self.visit(stmt.expr)
        self.environment.define(
            stmt.token.value, value, stmt.token.pos_start, stmt.token.pos_end
        )
        return None

    def visit_IfStmt(self, node):
        condition = self.visit(node.condition)
        if self.is_truthy(condition):
            self.visit(node.then_stmt)
        elif node.else_stmt is not None:
            self.visit(node.else_stmt)
        return None

    def visit_WhileStmt(self, node):
        while self.is_truthy(self.visit(node.condition)):
            self.visit(node.body)
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
        self.environment.assign(
            var_name, value, node.left.token.pos_start, node.left.token.pos_end
        )
        return value

    def visit_Identifier(self, node):
        return self.environment.get(
            node.token.pos_start, node.token.pos_end, node.value
        )

    def interpret(self):
        tree = self.parser.parse()
        if not tree:
            return None
        for node in tree:
            result = self.visit(node)
        return result
