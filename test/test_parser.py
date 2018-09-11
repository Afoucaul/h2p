import unittest
from h2p.parser import Expression, Application, parse


class TestH2PParser(unittest.TestCase):
    def test_simple_expression_application(self):
        inputData = "a b c"
        expected = Application(Expression("a"), [Expression("b"), Expression("c")])
        result = parse(inputData)
        self.assertEqual(expected, result)

    def test_parenthesized_expression_application(self):
        inputData = "(a) b c"
        expected = Application(Expression(Application(Expression("a"), [])), [Expression("b"), Expression("c")])
        result = parse(inputData)
        self.assertEqual(expected, result)

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
