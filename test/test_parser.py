import unittest
from h2p.hast import (
        HExpression, 
        HApplication, 
        HValue, 
        HVariable, 
        HNumber, 
        HListEnumeration, 
        HListComprehension, 
        HListComprehensionProduction,
        HListComprehensionCondition,
        HRange, 
        HPattern,
        HOperator
        )
import h2p.parser
import h2p.lexer as lexer

def parse(text):
    return h2p.parser.parse(text, start='application')

class TestH2PParser(unittest.TestCase):
    def test_simple_expression_application(self):
        inputData = "a b c"
        expected = HApplication(
                HExpression(HVariable("a")), 
                [HExpression(HVariable("b")), HExpression(HVariable("c"))])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_infix_operator(self):
        inputData = "a > 15"
        expected = HApplication(HOperator(">"), 
                [
                    HExpression(HVariable("a")), 
                    HExpression(HValue(HNumber("15")))
                    ])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_parenthesized_expression_application(self):
        inputData = "(a) b c"
        expected = HApplication(HExpression(HApplication(
            HExpression(HVariable("a")), [])), 
            [HExpression(HVariable("b")), HExpression(HVariable("c"))])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_parenthesized_parameter_application(self):
        inputData = "a (b c) d"
        expected = HApplication(
                HExpression(HVariable("a")),
                [
                    HExpression(HApplication(
                        HExpression(HVariable("b")), [HExpression(HVariable("c"))])),
                    HExpression(HVariable("d"))
                    ])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_deeply_parenthesized_parameter_application(self):
        inputData = "a (b (c d)) e"
        expected = HApplication(
                HExpression(HVariable("a")),
                [
                    HExpression(HApplication(
                        HExpression(HVariable("b")), 
                        [HExpression(HApplication(
                            HExpression(HVariable("c")), [HExpression(HVariable("d"))]))])),
                    HExpression(HVariable("e"))
                    ])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_numerical_value(self):
        inputData = "6"
        expected = HApplication(HExpression(HValue(HNumber("6"))), [])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_list_enumeration(self):
        inputData = "[1, 2, 3, 4]"
        expected = HApplication(
                HExpression(
                    HValue(
                        HListEnumeration([
                            HApplication(HExpression(HValue(HNumber("1"))), []),
                            HApplication(HExpression(HValue(HNumber("2"))), []),
                            HApplication(HExpression(HValue(HNumber("3"))), []),
                            HApplication(HExpression(HValue(HNumber("4"))), [])
                            ])
                        )),
                    []
                )
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_infinite_range(self):
        inputData = "[1..]"
        expected = HApplication(
                HExpression(
                    HValue(
                        HRange(HApplication(HExpression(HValue(HNumber("1"))), []), None, None)
                        )
                    ),
                []
                )
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_infinite_range_with_step(self):
        inputData = "[1, 3..]"
        expected = HApplication(
                HExpression(
                    HValue(
                        HRange(
                            HApplication(HExpression(HValue(HNumber("1"))), []), 
                            None, 
                            HApplication(HExpression(HValue(HNumber("3"))), [])
                            )
                        )
                    ),
                []
                )
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_simple_comprehension(self):
        inputData = """[x | x <- [1..]]"""
        expected = HApplication(
                HExpression(
                    HValue(
                        HListComprehension(
                            HApplication(HExpression(HVariable("x")), []), 
                            [
                                HListComprehensionProduction(
                                    HPattern("x"), 
                                    HApplication(HExpression(HValue(
                                        HRange(HApplication(HExpression(HValue(
                                            HNumber("1")
                                            )), []), None, None)
                                    )), [])
                                    )
                                ]))), [])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_comprehension_with_two_productions(self):
        inputData = "[x | x <- [1..], y <- [1, 3..11]]"
        expected = HApplication(
                HExpression(
                    HValue(
                        HListComprehension(
                            HApplication(HExpression(HVariable("x")), []), 
                            [
                                HListComprehensionProduction(
                                    HPattern("x"), 
                                    HApplication(HExpression(HValue(
                                        HRange(HApplication(HExpression(HValue(
                                            HNumber("1")
                                            )), []), None, None)
                                    )), [])
                                    ),
                                HListComprehensionProduction(
                                    HPattern("y"), 
                                    HApplication(HExpression(HValue(
                                        HRange(HApplication(HExpression(HValue(
                                            HNumber("1")
                                            )), []),
                                            HApplication(HExpression(HValue(
                                                HNumber("11")
                                                )), []),
                                            HApplication(HExpression(HValue(
                                                HNumber("3")
                                            )), []))
                                    )), [])
                                    )
                                ]))), [])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_comprehension_with_two_productions_and_one_condition(self):
        inputData = "[x | x <- [1..], y <- [1, 3..11], x == 3]"
        expected = HApplication(
                HExpression(
                    HValue(
                        HListComprehension(
                            HApplication(HExpression(HVariable("x")), []), 
                            [
                                HListComprehensionProduction(
                                    HPattern("x"), 
                                    HApplication(HExpression(HValue(
                                        HRange(HApplication(HExpression(HValue(
                                            HNumber("1")
                                            )), []), None, None)
                                    )), [])
                                    ),
                                HListComprehensionProduction(
                                    HPattern("y"), 
                                    HApplication(HExpression(HValue(
                                        HRange(HApplication(HExpression(HValue(
                                            HNumber("1")
                                            )), []),
                                            HApplication(HExpression(HValue(
                                                HNumber("11")
                                                )), []),
                                            HApplication(HExpression(HValue(
                                                HNumber("3")
                                            )), []))
                                    )), [])
                                    ),
                                HListComprehensionCondition(
                                    HApplication(HOperator("=="),
                                        [
                                            HExpression(HVariable("x")),
                                            HExpression(HValue(HNumber("3")))
                                            ]
                                    ))
                                ]))), [])
        result = parse(inputData)
        self.assertEqual(expected, result)
        result = parse(inputData)
        self.assertEqual(expected, result)
