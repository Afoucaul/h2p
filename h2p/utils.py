import ast

def compare_ast(t1, t2):
    if type(t1) != type(t2):
        return False

    if isinstance(t1, list):
        return len(t1) == len(t2) and all(compare_ast(c1, c2) for c1, c2 in zip(t1, t2))

    if not isinstance(t1, ast.AST):
        return t1 == t2

    for k, c1 in t1.__dict__.items():
        try:
            c2 = t2.__dict__[k]
        except AttributeError:
            print("Attribute {} not found:".format(k), c2)
            return False

        if not compare_ast(c1, c2):
            print("Attribute {} differs:".format(k), c1, c2)
            return False

    return True
