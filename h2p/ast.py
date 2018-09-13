class HAST: 
    def __init__(self, *args):
        self.children = args

    def __repr__(self):
        return "{}({})".format(type(self).__name__, ", ".join(str(x) for x in self.children))

    def __eq__(self, other):
        return type(self) == type(other) and self.children == other.children

    def transpile(self):
        self


class HExpression(HAST): pass
class HNumber(HAST) : pass
class HApplication(HAST): pass
class HExpression(HAST): pass
class HPattern(HAST): pass
class HLambda(HAST): pass
class HValue(HAST): pass
class HVariable(HAST): pass
class HNumber(HAST): pass
class HOperator(HAST): pass
class HList(HAST): pass
class HEmptyList(HList): pass
class HListEnumeration(HList): pass


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
