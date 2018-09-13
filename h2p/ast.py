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
class Variable(AST): pass
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
