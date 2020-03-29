// DEBUG == Command.PUSH constant 0 ==
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.POP local 0 ==
@LCL
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
// DEBUG == label LOOP_START ==
(LOOP_START)
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
// DEBUG == Command.PUSH local 0 ==
@LCL
D=M
@0
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
// DEBUG == Command.POP local 0 ==
@LCL
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
// DEBUG == if-goto LOOP_START ==
@SP
AM=M-1
D=M
@LOOP_START
D;JNE
// DEBUG == Command.PUSH local 0 ==
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
