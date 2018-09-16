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
from h2p.transpiler import transpile
from h2p.parser import parse
import h2p.lexer as lexer
from h2p.utils import compare_ast

_print = print
def myprint(x, *args, **kwargs):
    if isinstance(x, ast.AST):
        astpretty.pprint(x, *args, **kwargs)
    else:
        _print(x, *args, **kwargs)
print = myprint


class TestH2PTranspiler(unittest.TestCase):
    def test_simple_expression_application(self):
        inputData = "9"
        expected = ast.Expr(ast.Num(9))
        result = transpile(inputData)

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
