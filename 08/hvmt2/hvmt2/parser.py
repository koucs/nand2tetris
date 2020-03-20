import re
from hvmt2.constants import Command

# command
A_COMMAND_REX = re.compile(r'^(add|sub|neg|eq|gt|lt|and|or|not)$')
# (push|pop) segment index
COMMAND_2ARGS_REX = re.compile(r'^(push|pop)\s+(argument|local|static|constant|this|that|pointer|temp)\s+(\d+)$')
# (label|goto|if-goto) xxx
PROGRAM_FLOW_COMMAND_REX = re.compile(r'^(label|goto|if-goto)\s+([a-zA-Z_.:][a-zA-Z0-9_.:]+)$')
# (function|call) f n
FUNCTION_COMMAND_REX = re.compile(r'^(function|call)\s+([a-zA-Z_.:][a-zA-Z0-9_.:]+)\s+(\d+)$')
# return
RETURN_COMMAND_REX = re.compile(r'^return$')


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
        self.command, self._matched, self._command_type = None, None, None
        self._arg1, self._arg2 = None, None

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

        self._matched = PROGRAM_FLOW_COMMAND_REX.match(command)
        if self._matched is not None:
            if self._matched.group(1) == "label":
                self._command_type = Command.LABEL
            elif self._matched.group(1) == "goto":
                self._command_type = Command.GOTO
            else:
                self._command_type = Command.IF
            self._arg1 = self._matched.group(2)
            return

        self._matched = FUNCTION_COMMAND_REX.match(command)
        if self._matched is not None:
            if self._matched.group(1) == "function":
                self._command_type = Command.FUNCTION
            else:
                self._command_type = Command.CALL
            self._arg1 = self._matched.group(2)
            self._arg2 = self._matched.group(3)
            return

        self._matched = RETURN_COMMAND_REX.match(command)
        if self._matched is not None:
            self._command_type = Command.RETURN
        return

    def arg1(self):
        return self._arg1

    def arg2(self):
        return self._arg2

    def _clear(self):
        self.command, self._matched, self._command_type = None, None, None
        self._arg1, self._arg2 = None, None
