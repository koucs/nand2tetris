from hack_vm_translator.constants import *
import os


class CodeWriter:
    def __init__(self, path, debug):
        self._f = open(path, "w")
        self._file_name = os.path.basename(path).split(".")[0]
        self._debug = debug
        self._jump_cnt = 0
        return

    def set_file_name(self, name):
        self._file_name = name

    def write_arithmetic(self, command):
        s = ""
        if self._debug:
            s += "// DEBUG == {} ==\n".format(command)

        if command in [ADD, SUB, AND, OR]:
            s += "@SP\nAM=M-1\nD=M\nA=A-1\n"
            if command == ADD:
                s += "M=D+M\n"
            elif command == SUB:
                s += "M=M-D\n"
            elif command == AND:
                s += "M=D&M\n"
            elif command == OR:
                s += "M=D|M\n"

        elif command in [NEG, NOT]:
            s += "@SP\nA=M-1\n"
            if command == NEG:
                s += "M=-M\n"
            if command == NOT:
                s += "M=!M\n"

        elif command in [EQ, GT, LT]:
            self._jump_cnt += 1
            s += "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@J{0}_{1}\nD;J{0}\n" \
                 "@SP\nA=M-1\nM=0\n(J{0}_{1})\n".format(command.upper(), str(self._jump_cnt))

        self._f.write(s)
        return

    def write_push_pop(self, command, segment, index):
        s = ""
        if self._debug:
            s += "// DEBUG == {} {} {} ==\n".format(command, segment, index)
        if command is Command.PUSH:
            s += self._push(segment, index)
        elif command is Command.POP:
            s += self._pop(segment, index)
        self._f.write(s)
        return

    segment_command_table = {LOCAL: "LCL", ARGUMENT: "ARG", THIS: "THIS", THAT: "THAT", TEMP: "R5"}

    def _push(self, segment, index):
        s = ""
        if segment == CONSTANT:
            s += "@{0}\nD=A\n".format(index)
        elif segment in [LOCAL, ARGUMENT, THIS, THAT]:
            s += "@{0}\nD=M\n@{1}\nA=D+A\nD=M\n".format(self.segment_command_table[segment], index)
        elif segment in [TEMP]:
            s += "@5\nD=A\n@{0}\nA=D+A\nD=M\n".format(index)
        elif segment in [POINTER]:
            s += "@3\nD=A\n@{0}\nA=D+A\nD=M\n".format(index)
        elif segment in [STATIC]:
            s = "@{0}.{1}\nD=M\n".format(self._file_name, index)

        # 最後に push asm command setを追加
        s += "@SP\n" \
             "A=M\n" \
             "M=D\n" \
             "@SP\n" \
             "M=M+1\n"
        return s

    def _pop(self, segment, index):
        s = ""
        if segment in [LOCAL, ARGUMENT, THIS, THAT]:
            s += "@{0}\nD=M\n@{1}\nD=D+A\n".format(self.segment_command_table[segment], index)
        elif segment in [TEMP]:
            s += "@5\nD=A\n@{0}\nD=D+A\n".format(index)
        elif segment in [POINTER]:
            s += "@3\nD=A\n@{0}\nD=D+A\n".format(index)
        elif segment in [STATIC]:
            s += "@{0}.{1}\nD=A\n".format(self._file_name, index)

        # 最後に pop asm command setを追加
        s += "@R13\n" \
             "M=D\n" \
             "@SP\n" \
             "AM=M-1\n" \
             "D=M\n" \
             "@R13\n" \
             "A=M\n" \
             "M=D\n"
        return s

    def close(self):
        self._f.close()
