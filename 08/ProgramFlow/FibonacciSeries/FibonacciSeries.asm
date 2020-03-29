// DEBUG == Command.PUSH argument 1 ==
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.POP pointer 1 ==
@3
D=A
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// DEBUG == Command.PUSH constant 0 ==
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.POP that 0 ==
@THAT
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// DEBUG == Command.PUSH constant 1 ==
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.POP that 1 ==
@THAT
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// DEBUG == Command.PUSH argument 0 ==
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 2 ==
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == sub ==
@SP
AM=M-1
D=M
A=A-1
M=M-D
// DEBUG == Command.POP argument 0 ==
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// DEBUG == label MAIN_LOOP_START ==
(MAIN_LOOP_START)
// DEBUG == Command.PUSH argument 0 ==
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == if-goto COMPUTE_ELEMENT ==
@SP
AM=M-1
D=M
@COMPUTE_ELEMENT
D;JNE
// DEBUG == goto END_PROGRAM ==
@END_PROGRAM
0;JMP
// DEBUG == label COMPUTE_ELEMENT ==
(COMPUTE_ELEMENT)
// DEBUG == Command.PUSH that 0 ==
@THAT
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH that 1 ==
@THAT
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == add ==
@SP
AM=M-1
D=M
A=A-1
M=D+M
// DEBUG == Command.POP that 2 ==
@THAT
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// DEBUG == Command.PUSH pointer 1 ==
@3
D=A
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 1 ==
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == add ==
@SP
AM=M-1
D=M
A=A-1
M=D+M
// DEBUG == Command.POP pointer 1 ==
@3
D=A
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// DEBUG == Command.PUSH argument 0 ==
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 1 ==
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == sub ==
@SP
AM=M-1
D=M
A=A-1
M=M-D
// DEBUG == Command.POP argument 0 ==
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// DEBUG == goto MAIN_LOOP_START ==
@MAIN_LOOP_START
0;JMP
// DEBUG == label END_PROGRAM ==
(END_PROGRAM)
