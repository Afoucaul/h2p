import ast

def compare_ast(t1, t2):
    if type(t1) != type(t2):
        return False

    for k, c1 in t1.__dict__.items():
        c2 = t2.__dict__[k]
        equals = ((isinstance(c1, ast.AST) and type(c1) == type(c2) and compare_ast(c1, c2))
                or c1 == c2)
        if not equals:
            return False

    return True
