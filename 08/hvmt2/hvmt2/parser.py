import re
from hvmt2.constants import Command

# command
A_COMMAND_REX = re.compile(r'^(add|sub|neg|eq|gt|lt|and|or|not)$')
# (push|pop) segment index
COMMAND_2ARGS_REX = re.compile(r'^(push|pop)\s+(argument|local|static|constant|this|that|pointer|temp)\s+(\d+)$')


class Parser:

    def __init__(self, path):
        f = open(path, 'r')
        self.lines = f.readlines()
        f.close()

        # Remove commentOut char ("//")
        self.lines = [com.split('//')[0] for com in self.lines]
        # Remove newline char from the input
        self.lines = [com.strip() for com in self.lines]
        # Remove empty string
        self.lines = list(filter(None, self.lines))
        self.last = len(self.lines)
        self.index = 0
        self.command = None
        self._matched = None
        self._command_type = None
        self._arg1 = None
        self._arg2 = None

    def has_more_commands(self):
        return self.index < self.last

    def command_type(self):
        return self._command_type

    def advance(self):
        self._clear()
        command = self.lines[self.index]
        self.command = command
        self.index += 1

        self._matched = A_COMMAND_REX.match(command)
        if self._matched is not None:
            self._command_type = Command.ARITHMETIC
            return
        self._matched = COMMAND_2ARGS_REX.match(command)
        if self._matched is not None:
            if self._matched.group(1) == "push":
                self._command_type = Command.PUSH
            else:
                self._command_type = Command.POP
            self._arg1 = self._matched.group(2)
            self._arg2 = self._matched.group(3)
            return
        return

    def arg1(self):
        return self._arg1

    def arg2(self):
        return self._arg2

    def _clear(self):
        self.command = None
        self._matched = None
        self._command_type = None
        self._arg1 = None
        self._arg2 = None
