from io import StringIO
import unittest
from unittest.mock import patch
from lox import Lexer, RTError, InvalidSyntaxError
from parser import Parser
from interpreter import Interpreter
from environment import Environment


class TestInterpreter(unittest.TestCase):
    def makeInterpreter(self, text):
        environment = Environment()
        lexer = Lexer("stdin", text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser, environment)
        return interpreter

    def test_expression0(self):
        interpreter = self.makeInterpreter("1;")
        result = interpreter.interpret()
        self.assertEqual(result, 1)

    def test_expression1(self):
        interpreter = self.makeInterpreter("1 + 1;")
        result = interpreter.interpret()
        self.assertEqual(result, 2)

    def test_expression2(self):
        interpreter = self.makeInterpreter("-1 + 1;")
        result = interpreter.interpret()
        self.assertEqual(result, 0)

    def test_expression3(self):
        interpreter = self.makeInterpreter("1 + (-1);")
        result = interpreter.interpret()
        self.assertEqual(result, 0)

    def test_expression4(self):
        interpreter = self.makeInterpreter("1 - 1;")
        result = interpreter.interpret()
        self.assertEqual(result, 0)

    def test_expression5(self):
        interpreter = self.makeInterpreter("1 - (-1);")
        result = interpreter.interpret()
        self.assertEqual(result, 2)

    def test_expression6(self):
        interpreter = self.makeInterpreter("-1 - 1;")
        result = interpreter.interpret()
        self.assertEqual(result, -2)

    def test_expression7(self):
        interpreter = self.makeInterpreter("-1 - (-1);")
        result = interpreter.interpret()
        self.assertEqual(result, 0)

    def test_expression8(self):
        interpreter = self.makeInterpreter("1 * 1;")
        result = interpreter.interpret()
        self.assertEqual(result, 1)

    def test_expression9(self):
        interpreter = self.makeInterpreter("-1 * 1;")
        result = interpreter.interpret()
        self.assertEqual(result, -1)

    def test_expression10(self):
        interpreter = self.makeInterpreter("1 * (-1);")
        result = interpreter.interpret()
        self.assertEqual(result, -1)

    def test_expression11(self):
        interpreter = self.makeInterpreter("-1 * (-1);")
        result = interpreter.interpret()
        self.assertEqual(result, 1)

    def test_expression12(self):
        interpreter = self.makeInterpreter("1 * 1 * -1 * 2 * -2;")
        result = interpreter.interpret()
        self.assertEqual(result, 4)

    def test_expression13(self):
        interpreter = self.makeInterpreter("10 / 5;")
        result = interpreter.interpret()
        self.assertEqual(result, 2)

    def test_expression14(self):
        interpreter = self.makeInterpreter("-10 / 5;")
        result = interpreter.interpret()
        self.assertEqual(result, -2)

    def test_expression15(self):
        interpreter = self.makeInterpreter("10 / (-5);")
        result = interpreter.interpret()
        self.assertEqual(result, -2)

    def test_expression16(self):
        interpreter = self.makeInterpreter("-10 / (-5);")
        result = interpreter.interpret()
        self.assertEqual(result, 2)

    def test_expression17(self):
        interpreter = self.makeInterpreter("1 + 1 / 2;")
        result = interpreter.interpret()
        self.assertEqual(result, 1.5)

    def test_expression18(self):
        interpreter = self.makeInterpreter("(1 + 1) / 2;")
        result = interpreter.interpret()
        self.assertEqual(result, 1)

    def test_expression19(self):
        interpreter = self.makeInterpreter("-1;")
        result = interpreter.interpret()
        self.assertEqual(result, -1)

    def test_expression20(self):
        interpreter = self.makeInterpreter("--1;")
        result = interpreter.interpret()
        self.assertEqual(result, 1)

    def test_expression21(self):
        interpreter = self.makeInterpreter("-(1 + 2 / 2);")
        result = interpreter.interpret()
        self.assertEqual(result, -2)

    def test_expression22(self):
        interpreter = self.makeInterpreter("1 * 2 - 3 / -5 + 0.8;")
        result = interpreter.interpret()
        self.assertEqual(result, 3.4000000000000004)

    # crafting interpreters 6.1
    def test_expression23(self):
        interpreter = self.makeInterpreter("0.1 * (0.2 * 0.3);")
        result = interpreter.interpret()
        self.assertEqual(result, 0.006)

    # crafting interpreters 6.1
    def test_expression24(self):
        interpreter = self.makeInterpreter("(0.1 * 0.2) * 0.3;")
        result = interpreter.interpret()
        self.assertEqual(result, 0.006000000000000001)

    def test_expression_division_by_zero(self):
        interpreter = self.makeInterpreter("2 / 0;")
        with self.assertRaises(RTError):
            interpreter.interpret()

    def test_no_expression(self):
        interpreter = self.makeInterpreter("             ")
        result = interpreter.interpret()
        self.assertEqual(result, None)

    def test_expression_invalid_syntax1(self):
        interpreter = self.makeInterpreter("1 +")
        with self.assertRaises(InvalidSyntaxError):
            interpreter.interpret()

    def test_expression_invalid_syntax2(self):
        # Prints wrong error msg --> update parser
        interpreter = self.makeInterpreter("1 1 1 -")
        with self.assertRaises(InvalidSyntaxError):
            interpreter.interpret()

    def test_expression_invalid_syntax3(self):
        interpreter = self.makeInterpreter("(")
        with self.assertRaises(InvalidSyntaxError):
            interpreter.interpret()

    def test_expression_invalid_syntax4(self):
        interpreter = self.makeInterpreter(")")
        with self.assertRaises(InvalidSyntaxError):
            interpreter.interpret()

    def test_expression_invalid_syntax5(self):
        interpreter = self.makeInterpreter("+6")
        with self.assertRaises(InvalidSyntaxError):
            interpreter.interpret()

    def test_expression_invalid_syntax6(self):
        interpreter = self.makeInterpreter("(1 + 1;")
        with self.assertRaises(InvalidSyntaxError):
            interpreter.interpret()

    @patch("sys.stdout", new_callable=StringIO)
    def test_variable_declaration1(self, mock_stdout):
        text = """
        var a = 1;
        print a;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_variable_declaration2(self, mock_stdout):
        text = """
        var a = 1;
        var b = -1;
        print a * b;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "-1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_variable_declaration3(self, mock_stdout):
        text = """
        var a;
        print a;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "nil\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_variable_declaration4(self, mock_stdout):
        text = """
        var a = nil;
        print a;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "nil\n")

    def test_variable_declaration_errors1(self):
        interpreter = self.makeInterpreter("var a")
        with self.assertRaises(InvalidSyntaxError):
            interpreter.interpret()

    def test_variable_declaration_errors2(self):
        interpreter = self.makeInterpreter("a;")
        with self.assertRaises(RTError):
            interpreter.interpret()

    @patch("sys.stdout", new_callable=StringIO)
    def test_variable_assignment1(self, mock_stdout):
        text = """
        var a;
        print a;
        a = 1;
        print a;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "nil\n1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_scope1(self, mock_stdout):
        text = """
        var a = 1;
        {
            var b = -1;
            print a * b;
        }
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "-1.0\n")

    def test_scope_errors1(self):
        text = """
        var a = 1;
        {
            var b = -1;
        }
        print a * b;
        """
        interpreter = self.makeInterpreter(text)
        with self.assertRaises(RTError):
            interpreter.interpret()

    def test_arithmetic_ops_errors1(self):
        text = """
        var a;
        var b = 1;
        print a + b;
        """
        interpreter = self.makeInterpreter(text)
        with self.assertRaises(RTError):
            interpreter.interpret()

    def test_arithmetic_ops_errors2(self):
        text = """
        print 1 + nil;
        """
        interpreter = self.makeInterpreter(text)
        with self.assertRaises(RTError):
            interpreter.interpret()


if __name__ == "__main__":
    unittest.main()
