// Box.asm  -- K = 23
// start row = K = 23 -> first word address = 16384 + 32*23 = 17120
// height = 20 rows, width = (23 mod 4)+1 = 4 words = 64 pixels

(MAIN)
    @KBD
    D=M
    @PRESSED
    D;JNE           // key down -> black
    @color
    M=0             // no key -> white
    @DRAW
    0;JMP
(PRESSED)
    @color
    M=-1            // all 16 bits = 1 = black
(DRAW)
    @17120          // 16384 + 32*23
    D=A
    @ptr
    M=D             
    @20
    D=A
    @rows
    M=D             // rows left = 20
(ROWLOOP)
    @ptr
    D=M
    @addr
    M=D             // addr = start of this row
    @4              // (K mod 4)+1
    D=A
    @cols
    M=D             // words left in this row
(COLLOOP)
    @color
    D=M
    @addr
    A=M
    M=D             // RAM[addr] = color
    @addr
    M=M+1
    @cols
    M=M-1
    D=M
    @COLLOOP
    D;JGT
    @32
    D=A
    @ptr
    M=D+M           // next row (+32 words)
    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT
    @MAIN
    0;JMP
