from hack_vm_translator.constants import *
import os

segment_command_table = {
    LOCAL: "LCL",
    ARGUMENT: "ARG",
    THIS: "THIS",
    THAT: "THAT",
    TEMP: "R5"
}


class CodeWriter:
    def __init__(self, path, debug):
        self._f = open(path, "w")
        self.file_name = os.path.basename(path).split(".")[0]
        self._debug = debug
        self._jump_cnt = 0
        return

    def set_file_name(self, name):
        self.file_name = name

    def write_arithmetic(self, command):
        if self._debug:
            self._f.write("// {}\n".format(command))

        if command in [ADD, SUB, AND, OR]:
            self._f.write("@SP\n"
                          "AM=M-1\n"
                          "D=M\n"
                          "A=A-1\n")
            if command == ADD:
                self._f.write("M=D+M\n")
            elif command == SUB:
                self._f.write("M=M-D\n")
            elif command == AND:
                self._f.write("M=D&M\n")
            elif command == OR:
                self._f.write("M=D|M\n")

        elif command in [NEG, NOT]:
            self._f.write("@SP\n"
                          "A=M-1\n")
            if command == NEG:
                self._f.write("M=-M\n")
            if command == NOT:
                self._f.write("M=!M\n")

        elif command in [EQ, GT, LT]:
            self._jump_cnt += 1
            self._f.write("@SP\n"
                          "AM=M-1\n"
                          "D=M\n"
                          "A=A-1\n"
                          "D=M-D\n"
                          "M=-1\n"
                          "@J{0}_{1}\n"
                          "D;J{0}\n"
                          "@SP\n"
                          "A=M-1\n"
                          "M=0\n"
                          "(J{0}_{1})\n".format(command.upper(), str(self._jump_cnt)))

        return

    def write_push_pop(self, command, segment, index):
        if self._debug:
            self._f.write("// {} {} {}\n".format(command, segment, index))
        if command is Command.PUSH:
            if segment == CONSTANT:
                self._f.write("@{0}\n"
                              "D=A\n".format(index))
            elif segment in [LOCAL, ARGUMENT, THIS, THAT]:
                self._f.write("@{0}\n"
                              "D=M\n"
                              "@{1}\n"
                              "A=D+A\n"
                              "D=M\n".format(segment_command_table[segment], index))
            elif segment in [TEMP]:
                self._f.write("@5\n"
                              "D=A\n"
                              "@{0}\n"
                              "A=D+A\n"
                              "D=M\n".format(index))
            elif segment in [POINTER]:
                self._f.write("@3\n"
                              "D=A\n"
                              "@{0}\n"
                              "A=D+A\n"
                              "D=M\n".format(index))
            elif segment in [STATIC]:
                self._f.write("@{0}.{1}\n"
                              "D=M\n".format(self.file_name, index))
            self._push()

        elif command is Command.POP:
            if segment in [LOCAL, ARGUMENT, THIS, THAT]:
                self._f.write("@{0}\n"
                              "D=M\n"
                              "@{1}\n"
                              "D=D+A\n"
                              "@R13\n"
                              "M=D\n"
                              "@SP\n"
                              "AM=M-1\n"
                              "D=M\n"
                              "@R13\n"
                              "A=M\n"
                              "M=D\n".format(segment_command_table[segment], index))
            elif segment in [TEMP]:
                self._f.write("@5\n"
                              "D=A\n"
                              "@{0}\n"
                              "D=D+A\n"
                              "@R13\n"
                              "M=D\n"
                              "@SP\n"
                              "AM=M-1\n"
                              "D=M\n"
                              "@R13\n"
                              "A=M\n"
                              "M=D\n".format(index))
            elif segment in [POINTER]:
                self._f.write("@3\n"
                              "D=A\n"
                              "@{0}\n"
                              "D=D+A\n"
                              "@R13\n"
                              "M=D\n"
                              "@SP\n"
                              "AM=M-1\n"
                              "D=M\n"
                              "@R13\n"
                              "A=M\n"
                              "M=D\n".format(index))
            elif segment in [STATIC]:
                self._f.write("@{0}.{1}\n"
                              "D=A\n"
                              "@R13\n"
                              "M=D\n"
                              "@SP\n"
                              "AM=M-1\n"
                              "D=M\n"
                              "@R13\n"
                              "A=M\n"
                              "M=D\n".format(self.file_name, index))
            return

    def _push(self):
        self._f.write("@SP\n"
                      "A=M\n"
                      "M=D\n"
                      "@SP\n"
                      "M=M+1\n")

    def _pop(self):
        self._f.write("@SP\n"
                      "AM=M-1\n"
                      "D=M\n")

    def close(self):
        self._f.close()
