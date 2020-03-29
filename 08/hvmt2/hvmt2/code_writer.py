from hvmt2.constants import *
import os


class CodeWriter:
    def __init__(self, path, debug):
        self._f = open(path, "w")
        self._file_name = os.path.basename(path).split(".")[0]
        self._debug = debug
        self._jump_cnt = 0
        self._ret_cnt = 0
        return

    def set_file_name(self, name):
        self._file_name = name
        self._ret_cnt = 0

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

    # Program-Flow Command
    def write_label(self, label):
        self._write("({0})\n".format(label), "label", [label])

    def write_goto(self, label):
        self._write("@{0}\n0;JMP\n".format(label), "goto", [label])

    def write_if(self, label):
        self._write("@SP\nAM=M-1\nD=M\n@{0}\nD;JNE\n".format(label), "if-goto", [label])

    # Function Calls Command
    def write_init(self):
        o = "@256\nD=A\n@SP\nM=D\n"
        # o += "@{0}\n0;JMP\n".format("Sys.init")
        self._write(o, "BOOTSTRAP CODE", [])
        self.write_call("Sys.init", "0")
        return

    def write_call(self, f_name, num_args):
        return_label = "{0}$ret.{1}".format(self._file_name, self._ret_cnt)
        self._ret_cnt += 1  ## count up the return-address counter

        o = "@{0}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(return_label)  # push return-address
        o += "@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"  # push LCL
        o += "@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"  # push ARG
        o += "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"  # push THIS
        o += "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"  # push THAT
        o += "@SP\nD=M\n@5\nD=D-A\n@{0}\nD=D-A\n@ARG\nM=D\n".format(num_args)  # ARG = SP-n-5
        o += "@SP\nD=M\n@LCL\nM=D\n"  # LCL = SP
        o += "@{0}\n0;JMP\n".format(f_name)  # goto f_name
        o += "({0})\n".format(return_label)  # (return_address) label
        self._write(o, "call", [f_name, num_args])
        return

    def write_function(self, f_name, num_locals):
        o = "({})\n".format(f_name)
        # Initialize @LCL+num_locals as 0
        for i in range(int(num_locals)):
            o += "@{0}\nD=A\n@LCL\nA=M+D\nM=0\n".format(i)
        self._write(o, "function", [f_name, num_locals])
        return

    def write_return(self):
        o = "@LCL\nD=M\n@R13\nM=D\n"  # FRAME -> R13
        o += "@R13\nD=M\n@5\nA=D-A\nD=M\n@R14\nM=D\n"  # RET ( *(FRAME-5) ) -> R14
        o += "@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M+1\n@SP\nM=D\n"  # *ARG = pop() , SP = ARG+1
        o += "@R13\nD=M\n@1\nA=D-A\nD=M\n@THAT\nM=D\n"  # THAT = *(FRAME-1)
        o += "@R13\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n"  # THIS = *(FRAME-2)
        o += "@R13\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n"  # ARG = *(FRAME-3)
        o += "@R13\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n"  # LCL = *(FRAME-4)
        o += "@R14\nA=M\n0;JMP\n"  # goto RET
        self._write(o, "return", [])
        return

    def _write(self, output, command, arg=None):
        s = str()
        if self._debug and arg is not None:
            s += "// DEBUG == {} {} ==\n".format(command, " ".join(arg))
        s += output
        self._f.write(s)
        return

    def close(self):
        self._f.close()
