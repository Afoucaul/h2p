tokens = (
        'IDENT', 
        'NUMBER',
        'PLUS',
        'MINUS',
        'STAR',
        'SLASH',
        'EQUALS',
        'LPAREN',
        'RPAREN',
        'LBRACK',
        'RBRACK',
        'DOLLAR'
        )

# Tokens 
t_PLUS = r'\+' 
t_MINUS = r'-' 
t_STAR = r'\*' 
t_SLASH = r'/' 
t_EQUALS = r'=' 
t_LPAREN = r'\(' 
t_RPAREN = r'\)' 
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_DOLLAR = r'\$'

t_IDENT = r'[a-zA-Z][a-zA-Z0-9]*' 

def t_NUMBER(t): 
    r'\d+' 
    try: 
        t.value = int(t.value) 
    except ValueError: 
        print("Integer value too large %d", t.value) 
        t.value = 0 
        return t 

# Ignored characters 
t_ignore = " \t\r\n" 

def t_error(t): 
    print("Illegal character '%s'" % t.value[0]) 
    t.lexer.skip(1)


import ply.lex as lex 
lexer = lex.lex()
