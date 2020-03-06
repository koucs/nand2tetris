import os
from hack_vm_translator.constants import Command
from enum import Enum

# arithmetic
ADD = "add"
SUB = "sub"
NEG = "neg"
EQ = "eq"
GT = "gt"
LT = "lt"
AND = "and"
OR = "or"
NOT = "not"
# segment
CONSTANT = "constant"
ARGUMENT = "argument"
LOCAL = "local"
STATIC = "static"
THIS = "this"
THAT = "that"
POINTER = "pointer"
TEMP = "temp"

cnt = 0

str = "@SP\n" \
      "A=M\n" \
      "D=M\n" \
      "A=A-1\n" \
      "D=M-D\n" \
      "M=-1\n" \
      "@EQ_End{0}\n" \
      "D;JEQ\n" \
      "@SP\n" \
      "A=M-1\n" \
      "M=0\n" \
      "(EQ_End{0})\n"

class CodeWriter:
    def __init__(self, path, debug):
        self._f = open(path, "w")
        self.file_name = None
        self._debug = debug
        return

    def set_file_name(self, name):
        self.file_name = name

    def write_arithmetic(self, command):
        if self._debug:
            self._f.write("// {}\n".format(command))

        self._pop()

        if command in [ADD, SUB, AND, OR]:
            self._f.write("@SP\n"
                          "M=M-1\n"
                          "A=M\n")
            if command == ADD:
                self._f.write("D=D+M\n")
            elif command == SUB:
                self._f.write("D=D-M\n")
            elif command == AND:
                self._f.write("D=D&M\n")
            elif command == OR:
                self._f.write("D=D|M\n")

        elif command in [NEG, NOT]:
            if command == NEG:
                self._f.write("D=-M\n")
            if command == NOT:
                self._f.write("D=!M\n")
        # elif command in [EQ, GT, LT]:
        self._push()
        return

    def write_push_pop(self, command, segment, index):
        if self._debug:
            self._f.write("// {} {} {}\n".format(command, segment, str(index)))
        if command is Command.PUSH and segment == CONSTANT:
            self._f.write("@{0}\n"
                          "D=A\n".format(str(index)))
            self._push()
        return

    def _push(self):
        self._f.write("@SP\n"
                      "A=M\n"
                      "M=D\n"
                      "@SP\n"
                      "M=M+1\n")

    def _pop(self):
        self._f.write("@SP\n"
                      "M=M-1\n"
                      "A=M\n"
                      "D=M\n")

    def close(self):
        self._f.close()
