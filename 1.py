import abc
import re


class non_terminal:
    def __int__(self, name, val, element, visit):
        self.name = name
        self.val = val
        self.element = element
        self.visit = visit

    def interpret(self, context):
        pass

    def set_visit(self):
        pass

    def visit(self):
        pass


class minus(non_terminal):
    def __int__(self):
        self.name = 'minus'
        self.val = -1

    def interpret(self, context):
        if context[0] == '-':
            print(context[0])
            valid = 1
            rem_context = context[1:]
        else:
            valid = 0
            rem_context = context
        return valid, rem_context


class digit(non_terminal):
    def __int__(self):
        self.name = 'digit'

    def interpret(self, context):
        m = re.match('[0-9]', context[0])
        if m is not None:
            self.val = context[0]
            if len(context) != 1:
                valid = 1
                rem_context = context[1:]
            else:
                valid = 0
                rem_context = None
            return valid, rem_context
        else:
            valid = 0
            rem_context = context
            return valid, rem_context


class operator1(non_terminal):
    def __int__(self):
        self.name = 'operator1'

    def interpret(self, context):
        if context[0] == '+' or context[0] == '-':
            print(context[0])
            self.val = context[0]
            valid = 1
            rem_context = context[1:len(context)]
            return valid, rem_context


class operator2(non_terminal):
    def __int__(self):
        self.name = 'operator2'

    def interpret(self, context):
        if context[0] == '*' or context[0] == '/':
            self.val = context[0]
            valid = 1
            rem_context = context[1:len(context)]
            return valid, rem_context
        else:
            valid = 0
            rem_context = context
            return valid, rem_context


class decpoint(non_terminal):
    def __int__(self):
        self.name = 'decpoint'

    def interpret(self, context):
        if context[0] == '.':
            self.val = context[0]
            valid = 1
            rem_context = context[1:]
            return valid, rem_context
        valid = 0
        rem_context = context
        return valid, rem_context


class number(non_terminal):
    def __int__(self):
        self.name = 'number'

    def interpret(self, context):
        t = digit()
        av = ''
        a, b = t.interpret(context)
        if a == 1:
            av = av + t.val
        while a == 1:
            t = digit()
            a, b = t.interpret(b)
            if a == 1:
                av = av + t.val
        if b is not None:
            t = decpoint()
            a, b = t.interpret(b)
            if a == 1:
                av = av + t.val
        else:
            av = av + t.val
            valid = 0
            rem_context = None
            # print(av)
            self.val = float(av)
            return valid, rem_context
        while a == 1:
            t = digit()
            a, b = t.interpret(b)
            if a == 1 or b is None:
                # print(t.val)
                av = av + t.val
        valid = 1
        rem_context = b
        #print(av)
        self.val = float(av)
        return valid, rem_context


class term(non_terminal):
    def __int__(self):
        self.name = 'term'

    def interpret(self, context):
        s = 0
        t = number()
        a, b = t.interpret(context)
        self.val = t.val
        while a == 1 and b is not None:
            t = operator2()
            a, b = t.interpret(b)
            if a == 1:
                if t.val == '*':
                    s = 1
                else:
                    s = 2
            if a != 1:
                a = 1
                break
            t = number()
            a, b = t.interpret(b)
            if s == 1:
                self.val = self.val * t.val
            elif s == 2:
                self.val = self.val / t.val
        valid = a
        rem_context = b
        print(self.val)
        return valid, rem_context


class expression(non_terminal):
    def __int__(self):
        self.name = 'expression'

    def interpret(self, context):
        # minus part
        s = 0
        t = minus()
        a, b = t.interpret(context)
        if a == 1:
            s = -1
        else:
            s = 1
        # term part
        t = term()
        a, b = t.interpret(b)
        self.val = s * t.val
        # [operator1 term]*

        while a == 1 and b is not None:
            t = operator1()
            a, b = t.interpret(b)
            if a == 1:
                if t.val == '+':
                    s = 1
                elif t.val == '-':
                    s = 2
            t = term()
            a, b = t.interpret(b)
            if s == 1:
                self.val = self.val + t.val
            elif s == 2:
                self.val = self.val - t.val
        valid = 1
        rem_context = b
        print(+self.val)
        return valid, rem_context

class vistor:
    def structure_vistor(self):
        pass
    def value_vistor(self):
        pass

e = expression()
v, rc = e.interpret('123.22*234*2.3-23')

e.set_visitor(structure_visitor())
e.visit()

e.set_visitor(value_visitor())
e.visit()

#n = number()
#v, rc = n.interpret('383.220')
