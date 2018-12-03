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
            #print(context[0])
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
        mat = re.match('[0-9]', context[0])
        if mat is not None:
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
        self.nelement = []
        ele = 0
        t = digit()
        av = ''
        va, rmc = t.interpret(context)
        if va == 1:
            av = av + t.val
            self.nelement.append(t.val)
            self.nelement[ele] = "\t\t digit : " + t.val
            ele += 1
        while va == 1:
            t = digit()
            va, rmc = t.interpret(rmc)
            if va == 1:
                av = av + t.val
                self.nelement.append(t.val)
                self.nelement[ele] = "\t\t digit : " + t.val
                ele += 1
        if rmc is not None:
            t = decpoint()
            va, rmc = t.interpret(rmc)
            if va == 1:
                av = av + t.val
                self.nelement.append(t.val)
                self.nelement[ele] = "\t\t decpoint : " + t.val
                ele += 1
        else:
            av = av + t.val
            self.nelement.append(t.val)
            self.nelement[ele] = "\t\t digit : " + t.val
            ele += 1
            valid = 0
            rem_context = None
            # print(av)
            self.val = float(av)
            return valid, rem_context
        while va == 1:
            t = digit()
            va, rmc = t.interpret(rmc)
            if va == 1 or rmc is None:
                # print(t.val)
                av = av + t.val
                self.nelement.append(t.val)
                self.nelement[ele] = "\t\t digit : " + t.val
                ele += 1
        valid = 1
        rem_context = rmc
        # print(av)
        self.val = float(av)
        self.pval = "\tnumber : " + repr(self.val)
        return valid, rem_context

    def set_visitor(self, vstr, *args, **kwargs):
        vstr.visit(self.nelement, self.pval)



class term(non_terminal):
    def __int__(self):
        self.name = 'term'

    def interpret(self, context):
        self.telement = []
        ele = 0
        tmp = 0
        t = number()
        va, rmc = t.interpret(context)
        self.val = t.val
        t.val = int(t.val)
        self.telement.append(t.val)
        self.telement[ele] = "\t\t number : " + repr(t.val)
        ele += 1
        while va == 1 and rmc is not None:
            t = operator2()
            va, rmc = t.interpret(rmc)
            if va == 1:
                if t.val == '*':
                    tmp = 1
                    self.telement.append(t.val)
                    self.telement[ele] = "\t\t op2 : " + t.val
                    ele += 1
                else:
                    tmp = 2
                    self.telement.append(t.val)
                    self.telement[ele] = "\t\t op2 : " + t.val
                    ele += 1
            if va != 1:
                va = 1
                break
            t = number()
            va, rmc = t.interpret(rmc)
            if tmp == 1:
                self.val = self.val * t.val
                t.val = int(t.val)
                self.telement.append(t.val)
                self.telement[ele] = "\t\t number : " + repr(t.val)
                ele += 1
            elif tmp == 2:
                self.val = self.val / t.val
                t.val = int(t.val)
                self.telement.append(t.val)
                self.telement[ele] = "\t\t number : " + repr(t.val)
                ele += 1
        valid = va
        rem_context = rmc
        self.pval = int(self.val)
        self.pval = "\tterm : " + repr(self.pval)
        return valid, rem_context
    def set_visitor(self, vstr, *args, **kwargs):
        vstr.visit(self.telement, self.pval)


class expression(non_terminal):
    def __int__(self):
        self.name = 'expression'

    def interpret(self, context):
        self.element = []
        # minus part
        tmp = 0
        ele = 0
        t = minus()
        va, rmc = t.interpret(context)
        if va == 1:
            tmp = -1
            self.element.append(tmp)
            self.element[ele] = "\t\t minus : " + repr(tmp)
            ele += 1
        else:
            tmp = 1
        # term part
        t = term()
        va, rmc = t.interpret(rmc)
        self.val = tmp * t.val
        self.element.append(t.val)
        self.element[ele] = "\t\t term : " + repr(t.val)
        ele += 1
        # [operator1 term]*

        while va == 1 and rmc is not None:
            t = operator1()
            va, rmc = t.interpret(rmc)
            if va == 1:
                if t.val == '+':
                    tmp = 1
                elif t.val == '-':
                    tmp = 2
            self.element.append(t.val)
            self.element[ele] = "\t\t op1 : " + t.val
            ele += 1
            t = term()
            va, rmc = t.interpret(rmc)
            if t.val * 10 % 10 == 0:
                if t.val / 10 <= 10:
                    t.val = int(t.val)
            self.element.append(t.val)
            self.element[ele] = "\t\t term : " + repr(t.val)
            ele += 1
            if tmp == 1:
                self.val = self.val + t.val
            elif tmp == 2:
                self.val = self.val - t.val
        valid = 1
        rem_context = rmc
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


