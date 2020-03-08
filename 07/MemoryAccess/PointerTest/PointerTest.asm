// DEBUG == Command.PUSH constant 3030 ==
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.POP pointer 0 ==
@3
D=A
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
// DEBUG == Command.PUSH constant 3040 ==
@3040
D=A
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
// DEBUG == Command.PUSH constant 32 ==
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.POP this 2 ==
@THIS
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
// DEBUG == Command.PUSH constant 46 ==
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.POP that 6 ==
@THAT
D=M
@6
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// DEBUG == Command.PUSH pointer 0 ==
@3
D=A
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
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
// DEBUG == add ==
@SP
AM=M-1
D=M
A=A-1
M=D+M
// DEBUG == Command.PUSH this 2 ==
@THIS
D=M
@2
A=D+A
D=M
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
// DEBUG == Command.PUSH that 6 ==
@THAT
D=M
@6
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
