import unittest
import ast
import astpretty
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
import h2p.transpiler
from h2p.utils import compare_ast


def transpile(text, start='application'):
    return h2p.transpiler.transpile(text, start=start)


_print = print
def myprint(x, *args, **kwargs):
    if isinstance(x, ast.AST):
        try:
            astpretty.pprint(x, *args, **kwargs)
        except:
            print("Failed pretty printing AST")
            _print(x, *args, **kwargs)
    else:
        _print(x, *args, **kwargs)
print = myprint


class TestH2PTranspiler(unittest.TestCase):
    def test_simple_expression_application(self):
        inputData = "9"
        expected = ast.Expr(ast.Num(9))
        result = transpile(inputData)
        print(result)

        self.assertTrue(compare_ast(result, expected))

    def test_empty_list(self):
        inputData = "[]"
        expected = ast.Expr(ast.List([], None))
        result = transpile(inputData)

        self.assertTrue(compare_ast(result, expected))

    def test_simple_enumerated_list(self):
        inputData = "[1, 2, 3]"
        expected = ast.Expr(ast.List([ast.Num(1), ast.Num(2), ast.Num(3)], None))
        result = transpile(inputData)

        self.assertTrue(compare_ast(result, expected))

    def test_range_with_first_and_last(self):
        inputData = "[1..10]"
        expected = ast.Expr(ast.Call(ast.Name("range", None), [ast.Num(1), ast.Num(11)], None))
        result = transpile(inputData)

        self.assertTrue(compare_ast(result, expected))

    def test_range_with_first_second_and_last(self):
        inputData = "[1, 3..10]"
        expected = ast.Expr(ast.Call(
            ast.Name("range", None), 
            [ast.Num(1), ast.Num(11), ast.Num(2)], None))
        result = transpile(inputData)

        self.assertTrue(compare_ast(result, expected))

    def test_infinite_range(self):
        inputData = "[1..]"
        expected = ast.Expr(ast.Call(
            ast.Attribute(ast.Name("itertools", None), "count", None),
            [], [ast.keyword("start", ast.Num(1)), ast.keyword("step", ast.Num(1))]))
        result = transpile(inputData)

        self.assertTrue(compare_ast(result, expected))

    def test_infinite_range_with_step(self):
        inputData = "[1, 3..]"
        expected = ast.Expr(ast.Call(
            ast.Attribute(ast.Name("itertools", None), "count", None),
            [], [ast.keyword("start", ast.Num(1)), ast.keyword("step", ast.Num(2))]))
        result = transpile(inputData)

        self.assertTrue(compare_ast(result, expected))

    def test_simple_function_call(self):
        inputData = "f 1 2 3"
        expected = ast.Expr(ast.Call(
            ast.Name("f", None), 
            [ast.Num(1), ast.Num(2), ast.Num(3)], 
            []))
        result = transpile(inputData)

        self.assertTrue(compare_ast(result, expected))
