from lox import (
    TT_PLUS,
    TT_MINUS,
    TT_MUL,
    TT_DIV
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

    def visit_BinOp(self, node):
        if node.op.type == TT_PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TT_MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TT_MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TT_DIV:
            right = self.visit(node.right)
            if right == 0:
                pos_start = node.token.pos_start
                pos_end = node.token.pos_end
                raise RTError(pos_start, pos_end, "Division by zero")
            else:
                return self.visit(node.left) / right

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == TT_MINUS:
            return -self.visit(node.expr)

    def visit_PrintStmt(self, node):
        result = self.visit(node.expr)
        print(result)
        return None

    def visit_VarStmt(self, stmt):
        value = None
        if stmt.expr:
            value = self.visit(stmt.expr)
        self.environment[stmt.token.value] = value
        return None

    def visit_Assign(self, node):
        var_name = node.left.name
        if var_name in self.environment.values:
            value = self.visit(node.right)
            self.environment[var_name] = value
            return value
        raise RTError(node.left.token.pos_start, node.token.pos_end, f"Undefined variable '{var_name}'")

    def visit_Identifier(self, node):
        return self.environment.get(node.token.pos_start, node.token.pos_end, node.name)

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ""
        return self.visit(tree)
