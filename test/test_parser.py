import unittest
from h2p.parser import (
        Expression, 
        Application, 
        Value, 
        Variable, 
        Number, 
        ListEnumeration, 
        ListComprehension, 
        ListComprehensionProduction,
        ListComprehensionCondition,
        Range, 
        Pattern,
        Operator,
        parse
        )
import h2p.lexer as lexer


class TestH2PParser(unittest.TestCase):
    def test_simple_expression_application(self):
        inputData = "a b c"
        expected = Application(
                Expression(Variable("a")), 
                [Expression(Variable("b")), Expression(Variable("c"))])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_infix_operator(self):
        inputData = "a > 15"
        expected = Application(Operator(">"), 
                [
                    Expression(Variable("a")), 
                    Expression(Value(Number("15")))
                    ])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_parenthesized_expression_application(self):
        inputData = "(a) b c"
        expected = Application(Expression(Application(
            Expression(Variable("a")), [])), 
            [Expression(Variable("b")), Expression(Variable("c"))])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_parenthesized_parameter_application(self):
        inputData = "a (b c) d"
        expected = Application(
                Expression(Variable("a")),
                [
                    Expression(Application(
                        Expression(Variable("b")), [Expression(Variable("c"))])),
                    Expression(Variable("d"))
                    ])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_deeply_parenthesized_parameter_application(self):
        inputData = "a (b (c d)) e"
        expected = Application(
                Expression(Variable("a")),
                [
                    Expression(Application(
                        Expression(Variable("b")), 
                        [Expression(Application(
                            Expression(Variable("c")), [Expression(Variable("d"))]))])),
                    Expression(Variable("e"))
                    ])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_numerical_value(self):
        inputData = "6"
        expected = Application(Expression(Value(Number("6"))), [])
        result = parse(inputData)
        self.assertEqual(expected, result)

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
                            Application(Expression(Variable("x")), []), 
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
                            Application(Expression(Variable("x")), []), 
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

    def test_comprehension_with_two_productions_and_one_condition(self):
        inputData = "[x | x <- [1..], y <- [1, 3..11], x == 3]"
        expected = Application(
                Expression(
                    Value(
                        ListComprehension(
                            Application(Expression(Variable("x")), []), 
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
                                    ),
                                ListComprehensionCondition(
                                    Application(Operator("=="),
                                        [
                                            Expression(Variable("x")),
                                            Expression(Value(Number("3")))
                                            ]
                                    ))
                                ]))), [])
        result = parse(inputData)
        self.assertEqual(expected, result)
        result = parse(inputData)
        self.assertEqual(expected, result)
