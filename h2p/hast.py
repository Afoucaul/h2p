import ast

class HAST: 
    def __init__(self, *args):
        self.children = args

    def __repr__(self):
        return "{}({})".format(type(self).__name__, ", ".join(str(x) for x in self.children))

    def __eq__(self, other):
        return type(self) == type(other) and self.children == other.children

    def transpile(self):
        return type(self)(*[c.transpile() for c in self.children])


class HApplication(HAST):
    def __init__(self, application, arguments):
        super().__init__(application, arguments)
        self.application = application
        self.arguments = arguments

    def transpile(self):
        print("W - calling base transpile for node of type {}".format(type(self).__name__))
        return HApplication(
                self.application.transpile(), 
                [arg.transpile() for arg in self.arguments])


class HExpression(HAST): pass
class HNumber(HAST) : pass
class HExpression(HAST): pass
class HPattern(HAST): pass
class HLambda(HAST): pass
class HVariable(HAST): pass
class HOperator(HAST): pass
class HList(HAST): pass
class HEmptyList(HList): pass
class HListEnumeration(HList): pass


class HExpression(HAST):
    def __init__(self, body):
        super().__init__(body)
        self.body = body

    def transpile(self):
        if isinstance(self.body, HValue):
            return ast.Expr(self.body.transpile())


class HValue(HAST):
    def __init__(self, value_holder):
        super().__init__(value_holder)
        self.value_holder = value_holder

    def transpile(self):
        return self.value_holder.transpile()

    
class HNumber(HAST):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    def transpile(self):
        return ast.Num(self.value)


class HListComprehensionProduction(HAST):
    def __init__(self, pattern, source):
        super().__init__(pattern, source)
        self.pattern = pattern
        self.source = source


class HListComprehensionCondition(HAST):
    def __init__(self, condition):
        super().__init__(condition)
        self.condition = condition


class HListComprehension(HList):
    def __init__(self, element, suite):
        super().__init__(element, suite)
        self.element = element
        self.suite = suite


class HRange(HList):
    def __init__(self, first, last, second):
        super().__init__(first, last, second)
        self.first = first
        self.last = last
        self.second = second