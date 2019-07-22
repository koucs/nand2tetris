// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
  @i
  M=1
  @sum
  M=0
  @R2
  M=0

(LOOP)
  @R1
  D=M
  // if R1 - i < 0
  @i
  D=D-M
  @END
  D;JLT

  // R2+=R0
  @R0
  D=M
  @R2
  M=D+M

  // i++
  @i
  M=M+1
  // goto LOOP
  @LOOP
  0;JMP

(END)
  @END
  0;JMP