class minus:
    def interpret(self, context):
        valid = True
        return valid, rem_context


class digit:
    def interpret(self, context):
        valid = True
        return valid, rem_context


class operator1:
    def interpret(self, context):
        valid = True
        return valid, rem_context


class operator2:
    def interpret(self, context):
        valid = True
        return valid, rem_context


class decpoint:
    def interpret(self, context):
        valid = True
        return valid, rem_context


class number:
    def interpret(self, context):
        valid = True
        return valid, rem_context


class term:
    def interpret(self, context):
        valid = True
        return valid, rem_context


class expression:
    def interpret(self, context):
        valid = True
        return valid, rem_context


e = expression()
v, rc = e.interpret('123.22*234*2.3-23')