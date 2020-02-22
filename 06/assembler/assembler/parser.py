import os
import re
from constants import *

A_COMMAND_REX = re.compile(r'^@([_.$:a-zA-Z0-9]+)')
L_COMMAND_REX = re.compile(r'^\(([_.$:a-zA-Z0-9]+)\)$')


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

        # current index
        self.index = 0
        # current command
        self.command = None
        self._command_type = None
        # current symbol
        self.symbol = None

    def has_more_commands(self):
        return self.index < self.last

    def advance(self):
        self.command = self.lines[self.index]
        self.index += 1

    def command_type(self):
        self._command_type = A_COMMAND_REX.match(self.command)
        if self._command_type is not None:
            return Command.A

        # self.command_type = self.c_command_rex.match(self.nowline)
        # if self.command_type is not None:
        #     return Command.A

        self._command_type = L_COMMAND_REX.match(self.command)
        if self._command_type is not None:
            return Command.L

        return 100


if __name__ == '__main__':
    exit()
