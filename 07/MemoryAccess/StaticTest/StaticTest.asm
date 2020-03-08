// DEBUG == Command.PUSH constant 111 ==
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 333 ==
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 888 ==
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.POP static 8 ==
@StaticTest.8
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// DEBUG == Command.POP static 3 ==
@StaticTest.3
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// DEBUG == Command.POP static 1 ==
@StaticTest.1
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// DEBUG == Command.PUSH static 3 ==
@StaticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH static 1 ==
@StaticTest.1
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
// DEBUG == Command.PUSH static 8 ==
@StaticTest.8
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
