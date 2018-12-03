class ComputerPart:
    def accept():
        pass


class Keyboard(ComputerPart):
    def accept(visitor):
        visitor.visit(self)  # different visitors perform different operations (call the visit() of visitor)


class Monitor(ComputerPart):
    def accept(visitor):
        visitor.visit(self)  # different visitors perform different operations (call the visit() of visitor)


class Mouse(ComputerPart):
    def accept(visitor):
        visitor.visit(self)  # different visitors perform different operations (call the visit() of visitor)


class Computer(ComputerPart):

    def __init__(self):
        self.parts = [Mouse(), Keyboard(), Monitor()]

    def accept(visitor):
        for p in self.parts:
            p.accept(visitor)
        visitor.visit(self)  # different visitors perform different operations (call the visit() of visitor)


class ComputerPartVisitor:
    def visit(part):
        pass


class DisplayVisitor(
    ComputerPartVisitor):  # we can design different visitors for different operations on computer parts
    def visit(part):
        if isinstance(part, Computer):
            print('Displaying computer...')  # do something on Computer
        elif isinstance(part, Mouse):
            print('Displaying mouse...')  # do something on Mouse
        elif isinstance(part, Keyboard):
            print('Displaying keyboard...')  # do something on Keyboard
        elif isinstance(part, Monitor):
            print('Displaying monitor...')  # do something on Monitor


class FixMonitorVisitor(ComputerPartVisitor):  # a spcific operation (fixing) for the monitor
    def visit(monitor):
        print('Monitor fixed.')

computer = Computer()
computer.accept(DisplayVisitor())