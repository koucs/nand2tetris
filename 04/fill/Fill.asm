// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// https://github.com/havivha/Nand2Tetris/blob/master/04/fill/Fill.asm

    @status
    M=-1        // [初期] status=0xFFFF
    D=0         // SETSCREEN 向けの パラメータ
    @SETSCREEN
    0;JMP

(LOOP)
    @KBD
    D=M         // D = current keyboard character
    @SETSCREEN
    D;JEQ       // D==0 の場合、 D=0 でそのまま @SETSCREEN 下に jump (white)
    D=-1        // D!=0 の場合、 D=-1 で @SETSCREEN 下に jump (black)
    
(SETSCREEN)     // Dレジスタの値で更新 (Set D=new status before jumping here)
    @ARG        // = @R2
    M=D         // Dレジスタの値を @ARG に退避
    @status     
    D=D-M       // D = newstatus - status (0-0=0 / FFFF-FFFF=0 で 0 となったら同じ値である)
    @LOOP
    D;JEQ       // newstatus == status(@status) の場合は何もせず　@LOOP へ
    
    @ARG
    D=M         // 退避させていた Dレジスタの値を D レジスタへ
    @status
    M=D         // status = ARG
    
    @SCREEN
    D=A         // D=Screen address
    @8192
    D=D+A       // D=Screen address (last)
    @i
    M=D         // i=SCREEN address (last)
    
(SETLOOP)    
    @i
    D=M-1
    M=D         // i=i-1
    @LOOP
    D;JLT       // if i<0 goto LOOP
    
    @status
    D=M         // D=status
    @i
    A=M         // A = i (=SCREEN address)
    M=D         // M[SCREEN ADRESS]=status
    @SETLOOP
    0;JMP
