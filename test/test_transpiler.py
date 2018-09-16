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


class TestH2PTranspiler(unittest.TestCase):
    def test_simple_expression_application(self):
        inputData = "9"
        expected = ast.Expr(ast.Num("9"))
        result = transpile(inputData)

        self.assertTrue(compare_ast(result, expected))
