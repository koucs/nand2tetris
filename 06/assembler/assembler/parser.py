import os
from enum import Enum


class Command(Enum):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3


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

        self.in_dir = os.path.dirname(path)  # path/to
        self.in_name = os.path.basename(path)  # *.asm
        self.out_name = os.path.splitext(self.in_name)[0] + ".hack"  # *.hack
        self.last = len(self.lines)

        # current index
        self.index = 0
        # current command
        self.command = None
        # current symbol
        self.symbol = None

    def has_more_commands(self):
        return self.index < self.last

    def advance(self):
        self.command = self.lines[self.index]
        self.index += 1

    # def command_type(self):
    #     return Command.A_COMMAND
    #


if __name__ == '__main__':
    exit()
