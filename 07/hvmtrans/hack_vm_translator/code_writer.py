from hack_vm_translator.constants import *


class CodeWriter:
    def __init__(self, path, debug):
        self._f = open(path, "w")
        self.file_name = None
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
        if command is Command.PUSH and segment == CONSTANT:
            self._f.write("@{0}\n"
                          "D=A\n".format(index))
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
