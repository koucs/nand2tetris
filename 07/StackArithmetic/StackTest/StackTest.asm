// DEBUG == Command.PUSH constant 17 ==
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 17 ==
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == eq ==
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@JEQ_1
D;JEQ
@SP
A=M-1
M=0
(JEQ_1)
// DEBUG == Command.PUSH constant 17 ==
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 16 ==
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == eq ==
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@JEQ_2
D;JEQ
@SP
A=M-1
M=0
(JEQ_2)
// DEBUG == Command.PUSH constant 16 ==
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 17 ==
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == eq ==
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@JEQ_3
D;JEQ
@SP
A=M-1
M=0
(JEQ_3)
// DEBUG == Command.PUSH constant 892 ==
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 891 ==
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == lt ==
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@JLT_4
D;JLT
@SP
A=M-1
M=0
(JLT_4)
// DEBUG == Command.PUSH constant 891 ==
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 892 ==
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == lt ==
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@JLT_5
D;JLT
@SP
A=M-1
M=0
(JLT_5)
// DEBUG == Command.PUSH constant 891 ==
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 891 ==
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == lt ==
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@JLT_6
D;JLT
@SP
A=M-1
M=0
(JLT_6)
// DEBUG == Command.PUSH constant 32767 ==
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 32766 ==
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == gt ==
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@JGT_7
D;JGT
@SP
A=M-1
M=0
(JGT_7)
// DEBUG == Command.PUSH constant 32766 ==
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 32767 ==
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == gt ==
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@JGT_8
D;JGT
@SP
A=M-1
M=0
(JGT_8)
// DEBUG == Command.PUSH constant 32766 ==
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 32766 ==
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == gt ==
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@JGT_9
D;JGT
@SP
A=M-1
M=0
(JGT_9)
// DEBUG == Command.PUSH constant 57 ==
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 31 ==
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 53 ==
@53
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
// DEBUG == Command.PUSH constant 112 ==
@112
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
// DEBUG == neg ==
@SP
A=M-1
M=-M
// DEBUG == and ==
@SP
AM=M-1
D=M
A=A-1
M=D&M
// DEBUG == Command.PUSH constant 82 ==
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == or ==
@SP
AM=M-1
D=M
A=A-1
M=D|M
// DEBUG == not ==
@SP
A=M-1
M=!M
