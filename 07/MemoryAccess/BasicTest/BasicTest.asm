// DEBUG == Command.PUSH constant 10 ==
@10
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
// DEBUG == Command.PUSH constant 21 ==
@21
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 22 ==
@22
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.POP argument 2 ==
@ARG
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
// DEBUG == Command.POP argument 1 ==
@ARG
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
// DEBUG == Command.PUSH constant 36 ==
@36
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.POP this 6 ==
@THIS
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
// DEBUG == Command.PUSH constant 42 ==
@42
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 45 ==
@45
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.POP that 5 ==
@THAT
D=M
@5
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
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
// DEBUG == Command.PUSH constant 510 ==
@510
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.POP temp 6 ==
@5
D=A
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
// DEBUG == Command.PUSH that 5 ==
@THAT
D=M
@5
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
// DEBUG == sub ==
@SP
AM=M-1
D=M
A=A-1
M=M-D
// DEBUG == Command.PUSH this 6 ==
@THIS
D=M
@6
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH this 6 ==
@THIS
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
// DEBUG == sub ==
@SP
AM=M-1
D=M
A=A-1
M=M-D
// DEBUG == Command.PUSH temp 6 ==
@5
D=A
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
