import re
from constants import *

# @xxx
A_COMMAND_REX = re.compile(r'^@([_.$:a-zA-Z0-9]+)')
# (xxx)
L_COMMAND_REX = re.compile(r'^\(([_.$:a-zA-Z0-9]+)\)$')
# dest = comp ; jump
C_COMMAND_REX = re.compile(r'^(([AMD]{1,3})=)?([-!]?[AMD01])([-+&|])?([01AMD])?(;)?(J.{2})?$')


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
        # ref: https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
        self.lines = list(filter(None, self.lines))
        self.last = len(self.lines)
        self.index = 0

        self._clear()

    def has_more_commands(self):
        return self.index < self.last

    def advance(self):

        self._clear()

        command = self.lines[self.index]
        self.command = command
        self.index += 1

        self._matched = A_COMMAND_REX.match(command)
        if self._matched is not None:
            self._command_type = Command.A
            self._symbol = self._matched.group(1)
            return
        self._matched = C_COMMAND_REX.match(command)
        if self._matched is not None:
            self._command_type = Command.C
            self._comp = ''.join(list(filter(None.__ne__, self._matched.group(3, 4, 5))))
            self._jump = self._matched.group(7)
            self._dest = self._matched.group(2)
            return
        self._matched = L_COMMAND_REX.match(command)
        if self._matched is not None:
            self._command_type = Command.L
            self._symbol = self._matched.group(1)
            return

    def command_type(self):
        return self._command_type

    def symbol(self):
        return self._symbol

    def dest(self):
        return self._dest

    def comp(self):
        return self._comp

    def jump(self):
        return self._jump

    def _clear(self):
        # current command
        self.command = None
        self._matched = None
        self._command_type = None

        # current symbol
        self._symbol = None

        # current command mnemonic
        self._dest = None
        self._comp = None
        self._jump = None


if __name__ == '__main__':
    exit()
