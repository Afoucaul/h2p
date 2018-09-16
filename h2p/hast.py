import ast

class HAST: 
    def __init__(self, *args):
        self.children = args

    def __repr__(self):
        return "{}({})".format(type(self).__name__, ", ".join(str(x) for x in self.children))

    def __eq__(self, other):
        return type(self) == type(other) and self.children == other.children

    def transpile(self):
        print("W - calling base transpile for node of type {}".format(type(self).__name__))
        return type(self)(*[c.transpile() for c in self.children])


class HNumber(HAST) : pass
class HExpression(HAST): pass
class HPattern(HAST): pass
class HLambda(HAST): pass
class HVariable(HAST): pass
class HOperator(HAST): pass


class HApplication(HAST):
    def __init__(self, function, arguments):
        super().__init__(function, arguments)
        self.function = function
        self.arguments = arguments

    def transpile(self):
        if self.arguments == []:
            return self.function.transpile()

        else:
            return HApplication(
                    self.application.transpile(), 
                    [arg.transpile() for arg in self.arguments])


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
        if str(int(value)) == value:
            value = int(value)
        else:
            value = float(value)
        self.value = value

    def transpile(self):
        return ast.Num(self.value)


class HList(HAST):
    def transpile(self):
        return self


class HListComprehension(HList):
    def __init__(self, element, suite):
        super().__init__(element, suite)
        self.element = element
        self.suite = suite


class HListComprehensionProduction(HAST):
    def __init__(self, pattern, source):
        super().__init__(pattern, source)
        self.pattern = pattern
        self.source = source


class HListComprehensionCondition(HAST):
    def __init__(self, condition):
        super().__init__(condition)
        self.condition = condition


class HRange(HList):
    def __init__(self, first, last, second):
        super().__init__(first, last, second)
        self.first = first
        self.last = last
        self.second = second

    def transpile(self):
        if self.last is not None:
            x = self.last if self.first is None else self.first
            y = None if self.first is None else self.last
            z = None if self.second is None else self.second
            args = [x]
            if y is not None:
                args.append(y)
            if z is not None:
                args.append(z)
            args = [a.transpile().value for a in args]

            # Operations to adjust range boundaries and step
            if len(args) >= 2:
                args[1].n += 1
            if len(args) == 3:
                args[2].n -= args[0].n

            return ast.Call(ast.Name("range", None), args, None)

        else:
            start = self.first.transpile().value
            step = ast.Num(1)
            if self.second is not None:
                step = self.second.transpile().value
                step.n -= start.n

            kw_start = ast.keyword('start', start)
            kw_step = ast.keyword('step', step)

            return ast.Call(
                    ast.Attribute(ast.Name("itertools", None), 'count', None),
                    [], [kw_start, kw_step])


class HEmptyList(HList):
    def transpile(self):
        return ast.List([], None)


class HListEnumeration(HList):
    def __init__(self, values):
        super().__init__(values)
        self.values = values

    def transpile(self):
        return ast.List([v.transpile().value for v in self.values], None)
