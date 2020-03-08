// DEBUG == Command.PUSH constant 7 ==
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 8 ==
@8
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
