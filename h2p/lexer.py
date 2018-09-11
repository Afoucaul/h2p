tokens = (
        'IDENT', 
        'NUMBER',
        'PLUS',
        'STAR',
        'SLASH',
        'EQUALS',
        'LPAREN',
        'RPAREN',
        'LBRACK',
        'RBRACK',
        'DOLLAR',
        'COMMA',
        'DOT',
        'BAR',
        'DASH',
        'LT',
        )

# Tokens 
t_PLUS = r'\+' 
t_STAR = r'\*' 
t_SLASH = r'/' 
t_EQUALS = r'=' 
t_LPAREN = r'\(' 
t_RPAREN = r'\)' 
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_DOLLAR = r'\$'
t_COMMA = r','
t_DOT = r'\.'
t_BAR = r'\|'
t_DASH = r'-'
t_LT = r'<'

t_IDENT = r'[a-zA-Z][a-zA-Z0-9]*' 
t_NUMBER = r'\d+'


# Ignored characters 
t_ignore = " \t\r\n" 

def t_error(t): 
    print("Illegal character '%s'" % t.value[0]) 
    t.lexer.skip(1)


import ply.lex as lex 
lexer = lex.lex()
