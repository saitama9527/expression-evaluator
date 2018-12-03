from abc import ABC, abstractmethod


class Expression(ABC):
    pass
    #@abstractmethod
    #interpret(context):  # return True or False
    #pass


class TerminalExpression(Expression):
    def __init__(self):
        self.data = data

    def interpret(context):
        return data in context

class OrExpression(Expression):
    def __init__(self, expr1, expr2):
                self.expr1, self.expr2 = expr1, expr2

    def interpret(context):
        return self.expr1.interpret or self.expr2.interpret

class AndExpression(Expression):
    def __init__(self, expr1, expr2):
        self.expr1, self.expr2 = expr1, expr2

    def interpret(context):
        return self.expr1.interpret and self.expr2.interpret

robert = TerminalExpression('Robert')
john = TerminalExpression('John')
julie = TerminalExpression('Julie')
married = TerminalExpression('Married')
is_male = OrExpression(robert, john)
is_married_woman = AndExpression(julie, married)
print('John is male? ' + is_male.interpret('John'))
print('Julie is a married woman? ' + is_married_woman.interpret('Married Julie'))