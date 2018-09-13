from .lexer import tokens
import ply.yacc as yacc 

from .ast import (
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
        p[0] = HApplication(p[2], [p[1], p[3]])
    elif len(p) == 3:
        p[0] = HApplication(p[1], p[2])
    elif len(p) == 2:
        p[0] = HApplication(p[1], [])


def p_expression(p):
    '''expression : IDENT
                  | value
                  | LPAREN application RPAREN'''
    if len(p) == 2:
        if type(p[1]) == HValue:
            p[0] = HExpression(p[1])
        else:
            p[0] = HExpression(HVariable(p[1]))

    elif len(p) == 4:
        p[0] = HExpression(p[2])


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
    if len(p) == 2:
        p[0] = HOperator(p[1])
    elif len(p) == 3:
        p[0] = HOperator(p[1] + p[2])


def p_lambda(p):
    '''lambda : IDENT'''
    # '''lambda : SLASH patterns EQUALS expression'''
    p[0] = Lambda(p[1])


def p_value(p):
    '''value : number
             | list'''
    p[0] = HValue(p[1])


def p_number(p):
    '''number : NUMBER'''
    p[0] = HNumber(p[1])


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
    p[0] = HListEnumeration(p[1])

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
    p[0] = HListComprehensionProduction(p[1], p[3])


def p_list_comprehension_condition(p):
    '''comprehension_condition : application'''
    p[0] = HListComprehensionCondition(p[1])
    

def p_pattern(p):
    '''pattern : IDENT'''
    p[0] = HPattern(p[1])


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
        p[0] = HRange(p[1], None, None)
    elif len(p) == 5:
        p[0] = HRange(p[1], p[4], None)
    elif len(p) == 6:
        p[0] = HRange(p[1], None, p[3])
    elif len(p) == 7:
        p[0] = HRange(p[1], p[6], p[3])


def p_list_comprehension(p):
    '''list_comprehension : application BAR comprehension_productions_and_conditions'''
    if len(p) == 4:
        p[0] = HListComprehension(p[1], p[3])





parser = yacc.yacc() 


def parse(text):
    return parser.parse(text)
