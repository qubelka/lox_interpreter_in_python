from io import StringIO
import unittest
from unittest.mock import patch
from lox import Lexer, RTError, InvalidSyntaxError, ErrorDetails
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

    def test_expression25(self):
        interpreter = self.makeInterpreter("1 == 1;")
        result = interpreter.interpret()
        self.assertEqual(result, "true")

    def test_expression26(self):
        interpreter = self.makeInterpreter("1 == 2;")
        result = interpreter.interpret()
        self.assertEqual(result, "false")

    def test_expression27(self):
        interpreter = self.makeInterpreter("1 != 1;")
        result = interpreter.interpret()
        self.assertEqual(result, "false")

    def test_expression28(self):
        interpreter = self.makeInterpreter("1 != 2;")
        result = interpreter.interpret()
        self.assertEqual(result, "true")

    def test_expression29(self):
        interpreter = self.makeInterpreter('"a" == "a";')
        result = interpreter.interpret()
        self.assertEqual(result, "true")

    def test_expression30(self):
        interpreter = self.makeInterpreter('"a" == "b";')
        result = interpreter.interpret()
        self.assertEqual(result, "false")

    def test_expression31(self):
        interpreter = self.makeInterpreter('"a" != "b";')
        result = interpreter.interpret()
        self.assertEqual(result, "true")

    def test_expression32(self):
        interpreter = self.makeInterpreter('"a" != "a";')
        result = interpreter.interpret()
        self.assertEqual(result, "false")

    def test_expression33(self):
        interpreter = self.makeInterpreter("nil == 1;")
        result = interpreter.interpret()
        self.assertEqual(result, "false")

    def test_expression34(self):
        interpreter = self.makeInterpreter('"a" == true;')
        result = interpreter.interpret()
        self.assertEqual(result, "false")

    def test_expression34(self):
        interpreter = self.makeInterpreter("false == -1;")
        result = interpreter.interpret()
        self.assertEqual(result, "false")

    def test_expression35(self):
        interpreter = self.makeInterpreter('"a" + "b";')
        result = interpreter.interpret()
        self.assertEqual(result, "ab")

    def test_expression36(self):
        interpreter = self.makeInterpreter("1 > 0;")
        result = interpreter.interpret()
        self.assertEqual(result, "true")

    def test_expression37(self):
        interpreter = self.makeInterpreter("0.1 >= 0;")
        result = interpreter.interpret()
        self.assertEqual(result, "true")

    def test_expression38(self):
        interpreter = self.makeInterpreter("1 < 1.1;")
        result = interpreter.interpret()
        self.assertEqual(result, "true")

    def test_expression39(self):
        interpreter = self.makeInterpreter("1 <= 1;")
        result = interpreter.interpret()
        self.assertEqual(result, "true")

    def test_expression40(self):
        interpreter = self.makeInterpreter("1 < 1;")
        result = interpreter.interpret()
        self.assertEqual(result, "false")

    def test_expression41(self):
        interpreter = self.makeInterpreter("1 > 1;")
        result = interpreter.interpret()
        self.assertEqual(result, "false")

    def test_expression_division_by_zero(self):
        interpreter = self.makeInterpreter("2 / 0;")
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(ErrorDetails.DIVISION_BY_ZERO, e.exception.args[2])

    def test_no_expression(self):
        interpreter = self.makeInterpreter("             ")
        result = interpreter.interpret()
        self.assertEqual(result, None)

    def test_expression_invalid_syntax1(self):
        interpreter = self.makeInterpreter("1 +")
        with self.assertRaises(InvalidSyntaxError) as e:
            interpreter.interpret()
        self.assertEqual(ErrorDetails.EXPECTED_NUMBER, e.exception.args[2])

    def test_expression_invalid_syntax2(self):
        interpreter = self.makeInterpreter("1 1 1 -")
        with self.assertRaises(InvalidSyntaxError) as e:
            interpreter.interpret()
        self.assertEqual(
            ErrorDetails.EXPECTED_SEMICOLON_AFTER_EXPRESSION, e.exception.args[2]
        )

    def test_expression_invalid_syntax3(self):
        interpreter = self.makeInterpreter("(")
        with self.assertRaises(InvalidSyntaxError) as e:
            interpreter.interpret()
        self.assertEqual(ErrorDetails.EXPECTED_NUMBER, e.exception.args[2])

    def test_expression_invalid_syntax4(self):
        interpreter = self.makeInterpreter(")")
        with self.assertRaises(InvalidSyntaxError) as e:
            interpreter.interpret()
        self.assertEqual(ErrorDetails.EXPECTED_NUMBER, e.exception.args[2])

    def test_expression_invalid_syntax5(self):
        interpreter = self.makeInterpreter("+6")
        with self.assertRaises(InvalidSyntaxError) as e:
            interpreter.interpret()
        self.assertEqual(ErrorDetails.EXPECTED_NUMBER, e.exception.args[2])

    def test_expression_invalid_syntax6(self):
        interpreter = self.makeInterpreter("(1 + 1;")
        with self.assertRaises(InvalidSyntaxError) as e:
            interpreter.interpret()
        self.assertEqual(ErrorDetails.EXPECTED_RPAREN, e.exception.args[2])

    def test_expression_invalid_types1(self):
        interpreter = self.makeInterpreter('1 == "a";')
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(ErrorDetails.BINARY_OPS_TYPE_ERROR, e.exception.args[2])

    def test_expression_invalid_types2(self):
        interpreter = self.makeInterpreter('"a" != -1;')
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(ErrorDetails.BINARY_OPS_TYPE_ERROR, e.exception.args[2])

    def test_expression_invalid_types3(self):
        interpreter = self.makeInterpreter('1 - "a";')
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(
            ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
            e.exception.args[2],
        )

    def test_expression_invalid_types3(self):
        interpreter = self.makeInterpreter('"a" * "b";')
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(
            ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
            e.exception.args[2],
        )

    def test_expression_invalid_types4(self):
        interpreter = self.makeInterpreter("nil / 7;")
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(
            ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
            e.exception.args[2],
        )

    def test_expression_invalid_types5(self):
        interpreter = self.makeInterpreter('"a" + 1;')
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(ErrorDetails.BINARY_OPS_TYPE_ERROR, e.exception.args[2])

    def test_expression_invalid_types6(self):
        interpreter = self.makeInterpreter('"a" < 5;')
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(
            ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
            e.exception.args[2],
        )

    def test_expression_invalid_types7(self):
        interpreter = self.makeInterpreter("5 <= nil;")
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(
            ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
            e.exception.args[2],
        )

    def test_expression_invalid_types8(self):
        interpreter = self.makeInterpreter('"aa" > "a";')
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(
            ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
            e.exception.args[2],
        )

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
        with self.assertRaises(InvalidSyntaxError) as e:
            interpreter.interpret()
        self.assertEqual(
            ErrorDetails.EXPECTED_SEMICOLON_AFTER_EXPRESSION, e.exception.args[2]
        )

    def test_variable_declaration_errors2(self):
        interpreter = self.makeInterpreter("a;")
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(
            f"{ErrorDetails.UNDEFINED_VARIABLE.value} 'a'", e.exception.args[2]
        )

    def test_variable_declaration_errors3(self):
        text = """
        var a = 1;
        var a = 2;
        """
        interpreter = self.makeInterpreter(text)
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(f"Variable 'a' already defined", e.exception.args[2])

    def test_variable_declaration_errors4(self):
        text = """
        var a;
        var a = 2;
        """
        interpreter = self.makeInterpreter(text)
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(f"Variable 'a' already defined", e.exception.args[2])

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
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(
            f"{ErrorDetails.UNDEFINED_VARIABLE.value} 'b'", e.exception.args[2]
        )

    def test_arithmetic_ops_errors1(self):
        text = """
        var a;
        var b = 1;
        print a + b;
        """
        interpreter = self.makeInterpreter(text)
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(
            ErrorDetails.BINARY_OPS_TYPE_ERROR,
            e.exception.args[2],
        )

    def test_arithmetic_ops_errors2(self):
        text = """
        print 1 + nil;
        """
        interpreter = self.makeInterpreter(text)
        with self.assertRaises(RTError) as e:
            interpreter.interpret()
        self.assertEqual(
            ErrorDetails.BINARY_OPS_TYPE_ERROR,
            e.exception.args[2],
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_if_stmt1(self, mock_stdout):
        text = """
        var x;
        if (true) {
            x = 1;
        } else {
            x = 2;
        }
        print x;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_if_stmt2(self, mock_stdout):
        text = """
        var x;
        if (false) {
            x = 1;
        } else {
            x = 2;
        }
        print x;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "2.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_if_stmt3(self, mock_stdout):
        text = """
        var x;
        if (true) {
            x = 1;
        }
        print x;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_if_stmt4(self, mock_stdout):
        text = """
        var x;
        if (false) {
            x = 1;
        }
        print x;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "nil\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_equality1(self, mock_stdout):
        text = """
        if (1 == 1) {
            print 1;
        }
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_equality2(self, mock_stdout):
        text = """
        if (1 != 1) {
            print 1;
        } else {
            print 0;
        }
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "0.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_equality3(self, mock_stdout):
        text = """
        var a = (1 == 1);
        print a;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "true\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_equality4(self, mock_stdout):
        text = """
        var a = 1 != 1;
        if (a) {
            print a;
        } else {
            print 0;
        }
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "0.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_comparisons1(self, mock_stdout):
        text = """
        var a = true;
        print !a;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "false\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_comparisons2(self, mock_stdout):
        text = """
        var a = true;
        print a == true;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "true\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_comparisons3(self, mock_stdout):
        text = """
        var a = true;
        print 1 == a;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "false\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_comparisons4(self, mock_stdout):
        text = """
        var a = 1;
        var b = -1;
        print a > b;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "true\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_comparisons5(self, mock_stdout):
        text = """
        var a = 1;
        var b = -1;
        if (a >= b) {
            print "a is greater than b";
        } else {
            print "a is less than b";
        }
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "a is greater than b\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_comments1(self, mock_stdout):
        text = """
        // sample input
        var a;
        if ("string") {
            a = 1;
            print (a == 1);
        }
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(mock_stdout.getvalue(), "true\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_multiline_strings1(self, mock_stdout):
        text = """
        var a = "
                hello
                world";

        print a;
        """
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()
        self.assertEqual(
            mock_stdout.getvalue(), "\n                hello\n                world\n"
        )


if __name__ == "__main__":
    unittest.main()
