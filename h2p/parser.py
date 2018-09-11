from .lexer import tokens
import ply.yacc as yacc 


class AST: 
    def __init__(self, *args):
        self.args = args

    def __repr__(self):
        return "{}({})".format(type(self).__name__, ", ".join(str(x) for x in self.args))

    def __eq__(self, other):
        return type(self) == type(other) and self.args == other.args


class Expression(AST): pass
class Number(AST) : pass
class Application(AST): pass
class Expression(AST): pass
class Lambda(AST): pass
class Value(AST): pass



def p_application(p):
    '''application : expression infix_operator expression
                   | expression expressions
                   | expression'''
    if len(p) == 4:
        p[0] = Application(p[2], [p[1], p[3]])
    elif len(p) == 3:
        p[0] = Application(p[1], p[2])
    elif len(p) == 2:
        p[0] = Application(p[1], [])


def p_expression(p):
    '''expression : IDENT
                  | value
                  | LPAREN application RPAREN'''
    if len(p) == 2:
        p[0] = Expression(p[1])

    elif len(p) == 4:
        p[0] = Expression(p[2])


def p_expressions(p):
    '''expressions : expression
                   | expressions expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]


def p_infix_operator(p):
    '''infix_operator : PLUS 
                      | MINUS 
                      | SLASH
                      | STAR'''
    p[0] = p[1]


def p_lambda(p):
    '''lambda : IDENT'''
    # '''lambda : SLASH patterns EQUALS expression'''
    p[0] = Lambda(p[1])


def p_value(p):
    '''value : NUMBER'''
    p[0] = Value(p[1])


parser = yacc.yacc() 


def parse(text):
    return parser.parse(text)
