import unittest
from h2p.parser import (
        Expression, 
        Application, 
        Value, 
        Number, 
        ListEnumeration, 
        ListComprehension, 
        ListComprehensionProduction,
        Range, 
        Pattern,
        Operator,
        parse
        )
import h2p.lexer as lexer


class TestH2PParser(unittest.TestCase):
    @unittest.skip
    def test_simple_expression_application(self):
        inputData = "a b c"
        expected = Application(Expression("a"), [Expression("b"), Expression("c")])
        result = parse(inputData)
        self.assertEqual(expected, result)

    @unittest.skip
    def test_infix_operator(self):
        inputData = "a > 15"
        expected = Application(Operator(">"), 
                [
                    Expression("a"), 
                    Expression(Value(Number("15")))
                    ])
        result = parse(inputData)
        self.assertEqual(expected, result)

    @unittest.skip
    def test_parenthesized_expression_application(self):
        inputData = "(a) b c"
        expected = Application(Expression(Application(Expression("a"), [])), [Expression("b"), Expression("c")])
        result = parse(inputData)
        self.assertEqual(expected, result)

    @unittest.skip
    def test_parenthesized_parameter_application(self):
        inputData = "a (b c) d"
        expected = Application(
                Expression("a"),
                [
                    Expression(Application(Expression("b"), [Expression("c")])),
                    Expression("d")
                    ])
        result = parse(inputData)
        self.assertEqual(expected, result)

    @unittest.skip
    def test_deeply_parenthesized_parameter_application(self):
        inputData = "a (b (c d)) e"
        expected = Application(
                Expression("a"),
                [
                    Expression(Application(
                        Expression("b"), 
                        [Expression(Application(Expression("c"), [Expression("d")]))])),
                    Expression("e")
                    ])
        result = parse(inputData)
        self.assertEqual(expected, result)

    @unittest.skip
    def test_numerical_value(self):
        inputData = "6"
        expected = Application(Expression(Value(Number("6"))), [])
        result = parse(inputData)
        self.assertEqual(expected, result)

    @unittest.skip
    def test_list_enumeration(self):
        inputData = "[1, 2, 3, 4]"
        expected = Application(
                Expression(
                    Value(
                        ListEnumeration([
                            Application(Expression(Value(Number("1"))), []),
                            Application(Expression(Value(Number("2"))), []),
                            Application(Expression(Value(Number("3"))), []),
                            Application(Expression(Value(Number("4"))), [])
                            ])
                        )),
                    []
                )
        result = parse(inputData)
        self.assertEqual(expected, result)

    @unittest.skip
    def test_infinite_range(self):
        inputData = "[1..]"
        expected = Application(
                Expression(
                    Value(
                        Range(Application(Expression(Value(Number("1"))), []), None, None)
                        )
                    ),
                []
                )
        result = parse(inputData)
        self.assertEqual(expected, result)

    @unittest.skip
    def test_infinite_range_with_step(self):
        inputData = "[1, 3..]"
        expected = Application(
                Expression(
                    Value(
                        Range(
                            Application(Expression(Value(Number("1"))), []), 
                            None, 
                            Application(Expression(Value(Number("3"))), [])
                            )
                        )
                    ),
                []
                )
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_simple_comprehension(self):
        inputData = """[x | x <- [1..]]"""
        expected = Application(
                Expression(
                    Value(
                        ListComprehension(
                            Application(Expression("x"), []), 
                            [
                                ListComprehensionProduction(
                                    Pattern("x"), 
                                    Application(Expression(Value(
                                        Range(Application(Expression(Value(
                                            Number("1")
                                            )), []), None, None)
                                    )), [])
                                    )
                                ]))), [])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_comprehension_with_two_productions(self):
        inputData = "[x | x <- [1..], y <- [1, 3..11]]"
        expected = Application(
                Expression(
                    Value(
                        ListComprehension(
                            Application(Expression("x"), []), 
                            [
                                ListComprehensionProduction(
                                    Pattern("x"), 
                                    Application(Expression(Value(
                                        Range(Application(Expression(Value(
                                            Number("1")
                                            )), []), None, None)
                                    )), [])
                                    ),
                                ListComprehensionProduction(
                                    Pattern("y"), 
                                    Application(Expression(Value(
                                        Range(Application(Expression(Value(
                                            Number("1")
                                            )), []),
                                            Application(Expression(Value(
                                                Number("11")
                                                )), []),
                                            Application(Expression(Value(
                                                Number("3")
                                            )), []))
                                    )), [])
                                    )
                                ]))), [])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def _test_comprehension_with_two_productions_and_two_conditions(self):
        inputData = "[x | x <- [1..], y <- [1, 3..11], 1]"
        expected = Application(
                Expression(
                    Value(
                        ListComprehension(
                            Application(Expression("x"), []), 
                            [
                                (
                                    Pattern("x"), 
                                    Range(Application(Expression(Value(Number("1"))), []), None, None)
                                    ),
                                (
                                    Pattern("y"), 
                                    Range(
                                        Application(Expression(Value(Number("1"))), []),
                                        Application(Expression(Value(Number("11"))), []),
                                        Application(Expression(Value(Number("3"))), [])
                                        )
                                    )
                                ],
                            None
                            )
                        )
                    ),
                []
                )
        result = parse(inputData)
        self.assertEqual(expected, result)
