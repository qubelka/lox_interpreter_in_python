from io import StringIO
import unittest
from unittest.mock import patch
from lexer import Lexer, RTError, InvalidSyntaxError, ErrorDetails
from parser import Parser
from interpreter import Interpreter


class TestInterpreter(unittest.TestCase):
    def makeInterpreter(self, text):
        interpreter = Interpreter()
        lexer = Lexer("stdin", text)
        parser = Parser(lexer)
        return interpreter.interpret(parser)

    def test_expression0(self):
        result = self.makeInterpreter("1;")
        self.assertEqual(result, 1)

    def test_expression1(self):
        result = self.makeInterpreter("1 + 1;")
        self.assertEqual(result, 2)

    def test_expression2(self):
        result = self.makeInterpreter("-1 + 1;")
        self.assertEqual(result, 0)

    def test_expression3(self):
        result = self.makeInterpreter("1 + (-1);")
        self.assertEqual(result, 0)

    def test_expression4(self):
        result = self.makeInterpreter("1 - 1;")
        self.assertEqual(result, 0)

    def test_expression5(self):
        result = self.makeInterpreter("1 - (-1);")
        self.assertEqual(result, 2)

    def test_expression6(self):
        result = self.makeInterpreter("-1 - 1;")
        self.assertEqual(result, -2)

    def test_expression7(self):
        result = self.makeInterpreter("-1 - (-1);")
        self.assertEqual(result, 0)

    def test_expression8(self):
        result = self.makeInterpreter("1 * 1;")
        self.assertEqual(result, 1)

    def test_expression9(self):
        result = self.makeInterpreter("-1 * 1;")
        self.assertEqual(result, -1)

    def test_expression10(self):
        result = self.makeInterpreter("1 * (-1);")
        self.assertEqual(result, -1)

    def test_expression11(self):
        result = self.makeInterpreter("-1 * (-1);")
        self.assertEqual(result, 1)

    def test_expression12(self):
        result = self.makeInterpreter("1 * 1 * -1 * 2 * -2;")
        self.assertEqual(result, 4)

    def test_expression13(self):
        result = self.makeInterpreter("10 / 5;")
        self.assertEqual(result, 2)

    def test_expression14(self):
        result = self.makeInterpreter("-10 / 5;")
        self.assertEqual(result, -2)

    def test_expression15(self):
        result = self.makeInterpreter("10 / (-5);")
        self.assertEqual(result, -2)

    def test_expression16(self):
        result = self.makeInterpreter("-10 / (-5);")
        self.assertEqual(result, 2)

    def test_expression17(self):
        result = self.makeInterpreter("1 + 1 / 2;")
        self.assertEqual(result, 1.5)

    def test_expression18(self):
        result = self.makeInterpreter("(1 + 1) / 2;")
        self.assertEqual(result, 1)

    def test_expression19(self):
        result = self.makeInterpreter("-1;")
        self.assertEqual(result, -1)

    def test_expression20(self):
        result = self.makeInterpreter("--1;")
        self.assertEqual(result, 1)

    def test_expression21(self):
        result = self.makeInterpreter("-(1 + 2 / 2);")
        self.assertEqual(result, -2)

    def test_expression22(self):
        result = self.makeInterpreter("1 * 2 - 3 / -5 + 0.8;")
        self.assertEqual(result, 3.4000000000000004)

    # crafting interpreters 6.1
    def test_expression23(self):
        result = self.makeInterpreter("0.1 * (0.2 * 0.3);")
        self.assertEqual(result, 0.006)

    # crafting interpreters 6.1
    def test_expression24(self):
        result = self.makeInterpreter("(0.1 * 0.2) * 0.3;")
        self.assertEqual(result, 0.006000000000000001)

    def test_expression25(self):
        result = self.makeInterpreter("1 == 1;")
        self.assertEqual(result, "true")

    def test_expression26(self):
        result = self.makeInterpreter("1 == 2;")
        self.assertEqual(result, "false")

    def test_expression27(self):
        result = self.makeInterpreter("1 != 1;")
        self.assertEqual(result, "false")

    def test_expression28(self):
        result = self.makeInterpreter("1 != 2;")
        self.assertEqual(result, "true")

    def test_expression29(self):
        result = self.makeInterpreter('"a" == "a";')
        self.assertEqual(result, "true")

    def test_expression30(self):
        result = self.makeInterpreter('"a" == "b";')
        self.assertEqual(result, "false")

    def test_expression31(self):
        result = self.makeInterpreter('"a" != "b";')
        self.assertEqual(result, "true")

    def test_expression32(self):
        result = self.makeInterpreter('"a" != "a";')
        self.assertEqual(result, "false")

    def test_expression33(self):
        result = self.makeInterpreter("nil == 1;")
        self.assertEqual(result, "false")

    def test_expression34(self):
        result = self.makeInterpreter('"a" == true;')
        self.assertEqual(result, "false")

    def test_expression34(self):
        result = self.makeInterpreter("false == -1;")
        self.assertEqual(result, "false")

    def test_expression35(self):
        result = self.makeInterpreter('"a" + "b";')
        self.assertEqual(result, "ab")

    def test_expression36(self):
        result = self.makeInterpreter("1 > 0;")
        self.assertEqual(result, "true")

    def test_expression37(self):
        result = self.makeInterpreter("0.1 >= 0;")
        self.assertEqual(result, "true")

    def test_expression38(self):
        result = self.makeInterpreter("1 < 1.1;")
        self.assertEqual(result, "true")

    def test_expression39(self):
        result = self.makeInterpreter("1 <= 1;")
        self.assertEqual(result, "true")

    def test_expression40(self):
        result = self.makeInterpreter("1 < 1;")
        self.assertEqual(result, "false")

    def test_expression41(self):
        result = self.makeInterpreter("1 > 1;")
        self.assertEqual(result, "false")

    def test_expression_division_by_zero(self):
        with self.assertRaises(RTError) as e:
            self.makeInterpreter("2 / 0;")
        self.assertEqual(ErrorDetails.DIVISION_BY_ZERO, e.exception.args[2])

    def test_no_expression(self):
        result = self.makeInterpreter("             ")
        self.assertEqual(result, None)

    def test_expression_invalid_syntax1(self):
        with self.assertRaises(InvalidSyntaxError) as e:
            self.makeInterpreter("1 +")
        self.assertEqual(ErrorDetails.EXPECTED_NUMBER, e.exception.args[2])

    def test_expression_invalid_syntax2(self):
        with self.assertRaises(InvalidSyntaxError) as e:
            self.makeInterpreter("1 1 1 -")
        self.assertEqual(
            ErrorDetails.EXPECTED_SEMICOLON_AFTER_EXPRESSION, e.exception.args[2]
        )

    def test_expression_invalid_syntax3(self):
        with self.assertRaises(InvalidSyntaxError) as e:
            self.makeInterpreter("(")
        self.assertEqual(ErrorDetails.EXPECTED_NUMBER, e.exception.args[2])

    def test_expression_invalid_syntax4(self):
        with self.assertRaises(InvalidSyntaxError) as e:
            self.makeInterpreter(")")
        self.assertEqual(ErrorDetails.EXPECTED_NUMBER, e.exception.args[2])

    def test_expression_invalid_syntax5(self):
        with self.assertRaises(InvalidSyntaxError) as e:
            self.makeInterpreter("+6")
        self.assertEqual(ErrorDetails.EXPECTED_NUMBER, e.exception.args[2])

    def test_expression_invalid_syntax6(self):
        with self.assertRaises(InvalidSyntaxError) as e:
            self.makeInterpreter("(1 + 1;")
        self.assertEqual(ErrorDetails.EXPECTED_RPAREN, e.exception.args[2])

    def test_expression_invalid_types1(self):
        with self.assertRaises(RTError) as e:
            self.makeInterpreter('1 == "a";')
        self.assertEqual(ErrorDetails.BINARY_OPS_TYPE_ERROR, e.exception.args[2])

    def test_expression_invalid_types2(self):
        with self.assertRaises(RTError) as e:
            self.makeInterpreter('"a" != -1;')
        self.assertEqual(ErrorDetails.BINARY_OPS_TYPE_ERROR, e.exception.args[2])

    def test_expression_invalid_types3(self):
        with self.assertRaises(RTError) as e:
            self.makeInterpreter('1 - "a";')
        self.assertEqual(
            ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
            e.exception.args[2],
        )

    def test_expression_invalid_types3(self):
        with self.assertRaises(RTError) as e:
            self.makeInterpreter('"a" * "b";')
        self.assertEqual(
            ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
            e.exception.args[2],
        )

    def test_expression_invalid_types4(self):
        with self.assertRaises(RTError) as e:
            self.makeInterpreter("nil / 7;")
        self.assertEqual(
            ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
            e.exception.args[2],
        )

    def test_expression_invalid_types5(self):
        with self.assertRaises(RTError) as e:
            self.makeInterpreter('"a" + 1;')
        self.assertEqual(ErrorDetails.BINARY_OPS_TYPE_ERROR, e.exception.args[2])

    def test_expression_invalid_types6(self):
        with self.assertRaises(RTError) as e:
            self.makeInterpreter('"a" < 5;')
        self.assertEqual(
            ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
            e.exception.args[2],
        )

    def test_expression_invalid_types7(self):
        with self.assertRaises(RTError) as e:
            self.makeInterpreter("5 <= nil;")
        self.assertEqual(
            ErrorDetails.CAN_APPLY_ARITHMETIC_OPERATIONS_ONLY_TO_NUMBERS,
            e.exception.args[2],
        )

    def test_expression_invalid_types8(self):
        with self.assertRaises(RTError) as e:
            self.makeInterpreter('"aa" > "a";')
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
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_variable_declaration2(self, mock_stdout):
        text = """
        var a = 1;
        var b = -1;
        print a * b;
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "-1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_variable_declaration3(self, mock_stdout):
        text = """
        var a;
        print a;
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "nil\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_variable_declaration4(self, mock_stdout):
        text = """
        var a = nil;
        print a;
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "nil\n")

    def test_variable_declaration_errors1(self):
        with self.assertRaises(InvalidSyntaxError) as e:
            self.makeInterpreter("var a")
        self.assertEqual(
            ErrorDetails.EXPECTED_SEMICOLON_AFTER_EXPRESSION, e.exception.args[2]
        )

    def test_variable_declaration_errors2(self):
        with self.assertRaises(RTError) as e:
            self.makeInterpreter("a;")
        self.assertEqual(
            f"{ErrorDetails.UNDEFINED_VARIABLE.value} 'a'", e.exception.args[2]
        )

    def test_variable_declaration_errors3(self):
        text = """
        var a = 1;
        var a = 2;
        """
        with self.assertRaises(RTError) as e:
            self.makeInterpreter(text)
        self.assertEqual(f"Variable 'a' already defined", e.exception.args[2])

    def test_variable_declaration_errors4(self):
        text = """
        var a;
        var a = 2;
        """
        with self.assertRaises(RTError) as e:
            self.makeInterpreter(text)
        self.assertEqual(f"Variable 'a' already defined", e.exception.args[2])

    @patch("sys.stdout", new_callable=StringIO)
    def test_variable_assignment1(self, mock_stdout):
        text = """
        var a;
        print a;
        a = 1;
        print a;
        """
        self.makeInterpreter(text)
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
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "-1.0\n")

    def test_scope_errors1(self):
        text = """
        var a = 1;
        {
            var b = -1;
        }
        print a * b;
        """
        with self.assertRaises(RTError) as e:
            self.makeInterpreter(text)
        self.assertEqual(
            f"{ErrorDetails.UNDEFINED_VARIABLE.value} 'b'", e.exception.args[2]
        )

    def test_arithmetic_ops_errors1(self):
        text = """
        var a;
        var b = 1;
        print a + b;
        """
        with self.assertRaises(RTError) as e:
            self.makeInterpreter(text)
        self.assertEqual(
            ErrorDetails.BINARY_OPS_TYPE_ERROR,
            e.exception.args[2],
        )

    def test_arithmetic_ops_errors2(self):
        text = """
        print 1 + nil;
        """
        with self.assertRaises(RTError) as e:
            self.makeInterpreter(text)
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
        self.makeInterpreter(text)
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
        self.makeInterpreter(text)
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
        self.makeInterpreter(text)
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
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "nil\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_equality1(self, mock_stdout):
        text = """
        if (1 == 1) {
            print 1;
        }
        """
        self.makeInterpreter(text)
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
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "0.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_equality3(self, mock_stdout):
        text = """
        var a = (1 == 1);
        print a;
        """
        self.makeInterpreter(text)
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
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "0.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_comparisons1(self, mock_stdout):
        text = """
        var a = true;
        print !a;
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "false\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_comparisons2(self, mock_stdout):
        text = """
        var a = true;
        print a == true;
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "true\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_comparisons3(self, mock_stdout):
        text = """
        var a = true;
        print 1 == a;
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "false\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_comparisons4(self, mock_stdout):
        text = """
        var a = 1;
        var b = -1;
        print a > b;
        """
        self.makeInterpreter(text)
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
        self.makeInterpreter(text)
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
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "true\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_multiline_strings1(self, mock_stdout):
        text = """
        var a = "
                hello
                world";

        print a;
        """
        self.makeInterpreter(text)
        self.assertEqual(
            mock_stdout.getvalue(), "\n                hello\n                world\n"
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_logical1(self, mock_stdout):
        text = """
        if (true and true) {
            print 1;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_logical2(self, mock_stdout):
        text = """
        if (true and false) {
            print 1;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch("sys.stdout", new_callable=StringIO)
    def test_logical3(self, mock_stdout):
        text = """
        if (false and false) {
            print 1;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch("sys.stdout", new_callable=StringIO)
    def test_logical4(self, mock_stdout):
        text = """
        if (true or true) {
            print 1;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_logical5(self, mock_stdout):
        text = """
        if (true or false) {
            print 1;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_logical6(self, mock_stdout):
        text = """
        if (false or false) {
            print 1;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch("sys.stdout", new_callable=StringIO)
    def test_logical_short_circuit1(self, mock_stdout):
        text = """
        var x = 1;
        true and (x = 2);
        print x;
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "2.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_logical_short_circuit2(self, mock_stdout):
        text = """
        var x = 1;
        false and (x = 2);
        print x;
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_logical_short_circuit3(self, mock_stdout):
        text = """
        var x = 1;
        true or (x = 2);
        print x;
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "1.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_logical_short_circuit4(self, mock_stdout):
        text = """
        var x = 1;
        false or (x = 2);
        print x;
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "2.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_while1(self, mock_stdout):
        text = """
        var x = 1;
        while (x < 5) {
            print x;
            x = x + 1;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "1.0\n2.0\n3.0\n4.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_while2(self, mock_stdout):
        text = """
        var x = 1;
        while (x < 1) {
            print x;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch("sys.stdout", new_callable=StringIO)
    def test_for1(self, mock_stdout):
        text = """
        for (var x = 0; x < 5; x = x + 1) {
            print x;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "0.0\n1.0\n2.0\n3.0\n4.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_for2(self, mock_stdout):
        text = """
        for (var x = 0; x < 0; x = x + 1) {
            print x;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch("sys.stdout", new_callable=StringIO)
    def test_for3(self, mock_stdout):
        text = """
        var x = 0;
        for (; x < 5; x = x + 1) {
            print x;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "0.0\n1.0\n2.0\n3.0\n4.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_for4(self, mock_stdout):
        text = """
        for (var x = 0; x < 5;) {
            print x;
            x = x + 1;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "0.0\n1.0\n2.0\n3.0\n4.0\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_for5(self, mock_stdout):
        text = """
        var x;
        for (x = 0; x < 5; x = x + 1) {
            print x;
        }
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "0.0\n1.0\n2.0\n3.0\n4.0\n")

    # crafting interpreters part 3
    @patch("sys.stdout", new_callable=StringIO)
    def test_function_declarations1(self, mock_stdout):
        text = """
        fun printSum(a, b) {
            print a + b;
        }
        printSum(1, -1);
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "0.0\n")

    # crafting interpreters part 3
    @patch("sys.stdout", new_callable=StringIO)
    def test_function_declarations2(self, mock_stdout):
        text = """
        fun outerFunction() {
            fun localFunction() {
                print "I'm local!";
            }

            localFunction();
        }
        outerFunction();
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "I'm local!\n")

    # crafting interpreters part 10
    @patch("sys.stdout", new_callable=StringIO)
    def test_function_declarations3(self, mock_stdout):
        text = """
        fun count(n) {
            if (n > 1) count(n - 1);
            print n;
        }

        count(3);
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "1.0\n2.0\n3.0\n")

    # crafting interpreters part 10
    @patch("sys.stdout", new_callable=StringIO)
    def test_function_declarations4(self, mock_stdout):
        text = """
        fun add(a, b, c) {
            print a + b + c;
        }
        add(1, 2, 3);
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "6.0\n")

    # crafting interpreters part 10
    @patch("sys.stdout", new_callable=StringIO)
    def test_function_declarations5(self, mock_stdout):
        text = """
        fun add(a, b, c) {
            print a + b + c;
        }
        print add;
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "<fn add>\n")

    # crafting interpreters part 10
    @patch("sys.stdout", new_callable=StringIO)
    def test_function_declarations6(self, mock_stdout):
        text = """
        fun sayHi(first, last) {
            print "Hi, " + first + " " + last + "!";
        }

        sayHi("Dear", "Reader");
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "Hi, Dear Reader!\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_function_declarations7(self, mock_stdout):
        text = """
        var a = 1;
        fun local_scope() {
            var a = -1;
            print a;
        }
        local_scope();
        print a;
        """
        self.makeInterpreter(text)
        self.assertEqual(mock_stdout.getvalue(), "-1.0\n1.0\n")

    # crafting interpreters part 10
    def test_function_declaration_errors1(self):
        text = """
        fun add(a, b, c) {
            print a + b + c;
        }
        add(1, 2, 3, 4);
        """
        with self.assertRaises(RTError) as e:
            self.makeInterpreter(text)
        self.assertEqual(
            "Expected 3 arguments, but got 4.",
            e.exception.args[2],
        )

    # crafting interpreters part 10
    def test_function_declaration_errors2(self):
        text = """
        fun add(a, b, c) {
            print a + b + c;
        }
        add(1, 2);
        """
        with self.assertRaises(RTError) as e:
            self.makeInterpreter(text)
        self.assertEqual(
            "Expected 3 arguments, but got 2.",
            e.exception.args[2],
        )

    def test_function_declaration_errors3(self):
        text = """
        fun local_scope() {
            var b = 1;
            print b;
        }
        local_scope();
        print b;
        """
        with self.assertRaises(RTError) as e:
            self.makeInterpreter(text)
        self.assertEqual(
            f"{ErrorDetails.UNDEFINED_VARIABLE.value} 'b'",
            e.exception.args[2],
        )


if __name__ == "__main__":
    unittest.main()
