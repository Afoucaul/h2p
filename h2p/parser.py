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
class Pattern(AST): pass
class Lambda(AST): pass
class Value(AST): pass
class Number(AST): pass
class List(AST): pass
class EmptyList(List): pass
class ListEnumeration(List): pass


class ListComprehension(List):
    def __init__(self, element, productions: [(str, List)], conditions):
        super().__init__(element, productions, conditions)
        self.element = element
        self.productions = productions
        self.confitions = conditions

class Range(List):
    def __init__(self, first, last, second):
        super().__init__(first, last, second)
        self.first = first
        self.last = last
        self.second = second




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
                      | DASH 
                      | SLASH
                      | STAR'''
    p[0] = p[1]


def p_lambda(p):
    '''lambda : IDENT'''
    # '''lambda : SLASH patterns EQUALS expression'''
    p[0] = Lambda(p[1])


def p_value(p):
    '''value : number
             | list'''
    p[0] = Value(p[1])


def p_number(p):
    '''number : NUMBER'''
    p[0] = Number(p[1])


def p_list(p):
    '''list : LBRACK list_description RBRACK
            | LBRACK RBRACK'''
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = EmptyList()


def p_list_description(p):
    '''list_description : list_enumeration
                        | list_comprehension
                        | range'''
    p[0] = p[1]


def p_list_enumeration(p):
    '''list_enumeration : list_values'''
    p[0] = ListEnumeration(p[1])


def p_list_comprehension(p):
    '''list_comprehension : application BAR comprehension_productions
                          | application BAR comprehension_productions COMMA comprehension_conditions
                          '''
    if len(p) == 4:
        p[0] = ListComprehension(p[1], p[3], None)
    elif len(p) == 6:
        p[0] = ListComprehension(p[1], p[3], p[5])

def p_comprehension_productions(p):
    '''comprehension_productions : comprehension_production
                                 | comprehension_production COMMA comprehension_productions'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_comprehension_production(p):
    '''comprehension_production : pattern LT DASH list'''
    p[0] = (p[1], p[4])


def p_comprehension_conditions(p):
    '''comprehension_conditions : comprehension_condition
                                 | comprehension_condition COMMA comprehension_conditions'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_comprehension_condition(p):
    '''comprehension_condition : pattern LT DASH list'''
    p[0] = (p[1], p[4])
    

def p_pattern(p):
    '''pattern : IDENT'''
    p[0] = Pattern(p[1])


def p_list_values(p):
    '''list_values : application
                   | application COMMA list_values'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]


def p_range(p):
    '''range : application DOT DOT 
             | application DOT DOT application
             | application COMMA application DOT DOT
             | application COMMA application DOT DOT application'''
    if len(p) == 4:
        p[0] = Range(p[1], None, None)
    elif len(p) == 5:
        p[0] = Range(p[1], p[4], None)
    elif len(p) == 6:
        p[0] = Range(p[1], None, p[3])
    elif len(p) == 7:
        p[0] = Range(p[1], p[3], p[6])




parser = yacc.yacc() 


def parse(text):
    return parser.parse(text)
