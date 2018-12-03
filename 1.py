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

    def set_visitor(self, *args, **kwargs):
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
            # print(context[0])
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
        self.element = []
        ele = 0
        t = digit()
        av = ''
        a, b = t.interpret(context)
        if a == 1:
            av = av + t.val
            self.element.append(t.val)
            self.element[ele] = "\t\t digit1 : " + t.val
            ele += 1
        while a == 1:
            t = digit()
            a, b = t.interpret(b)
            if a == 1:
                av = av + t.val
                self.element.append(t.val)
                self.element[ele] = "\t\t digit2 : " + t.val
                ele += 1
        if b is not None:
            t = decpoint()
            a, b = t.interpret(b)
            if a == 1:
                av = av + t.val
                self.element.append(t.val)
                self.element[ele] = "\t\t decpoint : " + t.val
                ele += 1
        else:
            av = av + t.val
            self.element.append(t.val)
            self.element[ele] = "\t\t digit4 : " + repr(t.val)
            ele += 1
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
        # print(av)
        self.val = float(av)
        self.val = "\tnumber : " + repr(self.val)
        return valid, rem_context

    def set_visitor(self, vstr, *args, **kwargs):
        vstr.visit(self.element, self.val)


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
        # print(self.val)
        return valid, rem_context


class expression(non_terminal):
    def __int__(self):
        self.name = 'expression'

    def interpret(self, context):
        self.element = []
        # minus part
        s = 0
        ele = 0
        t = minus()
        a, b = t.interpret(context)
        if a == 1:
            s = -1
            self.element.append(s)
            self.element[ele] = "\t\t minus : " + repr(s)
            ele += 1
        else:
            s = 1
        # term part
        t = term()
        a, b = t.interpret(b)
        self.val = s * t.val
        self.element.append(t.val)
        self.element[ele] = "\t\t term : " + repr(t.val)
        ele += 1
        # [operator1 term]*

        while a == 1 and b is not None:
            t = operator1()
            a, b = t.interpret(b)
            if a == 1:
                if t.val == '+':
                    s = 1
                elif t.val == '-':
                    s = 2
            self.element.append(t.val)
            self.element[ele] = "\t\t op1 : " + t.val
            ele += 1
            t = term()
            a, b = t.interpret(b)
            if t.val * 10 % 10 == 0:
                if t.val / 10 <= 10:
                    t.val = int(t.val)
            self.element.append(t.val)
            self.element[ele] = "\t\t term : " + repr(t.val)
            ele += 1
            if s == 1:
                self.val = self.val + t.val
            elif s == 2:
                self.val = self.val - t.val
        valid = 1
        rem_context = b
        self.val = "\texpression : " + repr(self.val)
        # print(+self.val)
        return valid, rem_context

    def set_visitor(self, vstr, *args, **kwargs):
        vstr.visit(self.element, self.val)

    def visit(self):
        pass


class visitor:
    def visit(part):
        pass


class structure_visitor(visitor):
    def visit(self, part, val):
        print("Structure:")
        for n in part:
            print(n)
        print(val)


class value_visitor(visitor):
    def visit(self, part, val):
        print("Value:")
        print(val)


e = expression()
v, rc = e.interpret('123.22*234*2.3-23')
e.set_visitor(structure_visitor())
e.visit()
e.set_visitor(value_visitor())
e.visit()