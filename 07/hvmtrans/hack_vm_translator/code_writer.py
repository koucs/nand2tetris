import os
from hack_vm_translator.constants import Command

ARITHMETIC_ADD_COMMAND = "add"
PUSH_CONSTANT_SEGMENT = "constant"


class CodeWriter:
    def __init__(self, path):
        self._f = open(path, "w")
        self.file_name = None
        return

    def set_file_name(self, name):
        self.file_name = name

    def write_arithmetic(self, command):
        if command == ARITHMETIC_ADD_COMMAND:
            self._f.write("@SP\n"
                          "M=M-1\n"
                          "A=M\n"
                          "D=M\n"
                          "@SP\n"
                          "M=M-1\n"
                          "A=M\n"
                          "D=D+M\n"
                          "@SP\n"
                          "A=M\n"
                          "M=D\n"
                          "@SP\n"
                          "M=M+1\n")
        return

    def write_push_pop(self, command, segment, index):
        if command is Command.PUSH and segment == PUSH_CONSTANT_SEGMENT:
            self._f.write("@{0}\n"
                          "D=A\n"
                          "@SP\n"
                          "A=M\n"
                          "M=D\n"
                          "@SP\n"
                          "M=M+1\n".format(str(index)))
        # elif command is Command.POP:
        #     self._f.write("@SP\n"
        #                   "A=M\n"
        #                   "D=M\n"
        #                   "@SP\n"
        #                   "M=M-1\n".format(str(index)))
        return

    def close(self):
        self._f.close()
