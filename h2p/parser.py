from .lexer import tokens
import ply.yacc as yacc 


class AST: 
    def __init__(self, *args):
        self.children = args

    def __repr__(self):
        return "{}({})".format(type(self).__name__, ", ".join(str(x) for x in self.children))

    def __eq__(self, other):
        return type(self) == type(other) and self.children == other.children


class Expression(AST): pass
class Number(AST) : pass
class Application(AST): pass
class Expression(AST): pass
class Pattern(AST): pass
class Lambda(AST): pass
class Value(AST): pass
class Number(AST): pass
class Operator(AST): pass
class List(AST): pass
class EmptyList(List): pass
class ListEnumeration(List): pass


class ListComprehensionProduction(AST):
    def __init__(self, pattern: Pattern, source: List):
        super().__init__(pattern, source)
        self.pattern = pattern
        self.source = source


class ListComprehensionCondition(AST):
    def __init__(self, condition):
        super().__init__(condition)
        self.condition = condition


class ListComprehension(List):
    def __init__(self, element, suite):
        super().__init__(element, suite)
        self.element = element
        self.suite = suite


class Range(List):
    def __init__(self, first, last, second):
        super().__init__(first, last, second)
        self.first = first
        self.last = last
        self.second = second


def log(rule):
    def wrapped(p):
        print("\nIn {}:\n  {}".format(rule.__name__[2:], p.stack))
        result = rule(p)
        print("  {}".format(p[0]))
        return result

    wrapped.__name__ = rule.__name__
    wrapped.__doc__ = rule.__doc__
    return wrapped


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
                      | STAR
                      | LT
                      | GT
                      | EQUALS EQUALS'''
    p[0] = Operator(p[1])


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

def p_list_comprehension_productions_and_conditions(p):
    '''comprehension_productions_and_conditions : comprehension_production_or_condition
                                                | comprehension_productions_and_conditions COMMA comprehension_production_or_condition
                                                '''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]

def p_list_comprehension_production_or_condition(p):
    '''comprehension_production_or_condition : comprehension_production
                                             | comprehension_condition'''
    p[0] = p[1]

def p_list_comprehension_production(p):
    '''comprehension_production : pattern LEFTARROW application'''
    p[0] = ListComprehensionProduction(p[1], p[3])


def p_list_comprehension_condition(p):
    '''comprehension_condition : application'''
    p[0] = ListComprehensionCondition(p[1])
    

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
        p[0] = Range(p[1], p[6], p[3])


def p_list_comprehension(p):
    '''list_comprehension : application BAR comprehension_productions_and_conditions'''
    if len(p) == 4:
        p[0] = ListComprehension(p[1], p[3])





parser = yacc.yacc() 


def parse(text):
    return parser.parse(text)
