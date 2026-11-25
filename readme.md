# Nand to Tetris Capstone: Make the Computer Draw a Box

- Name: <your name>
- Roll no: 2501730123
- K = 23
- Box: starts at row 23, 20 rows tall, 64 pixels wide (4 words), from the left edge
- Extra assembler feature (K mod 3 = 2): warning when a label is defined twice

## Files
- `assembler.py`: two-pass Hack assembler. Usage: `python assembler.py Prog.asm 23`
- `Box.asm` / `Box.hack`: the box program, assembled with my own assembler
- `Add`, `Max`, `Rect`, `Pong` (.asm/.hack): test programs, output matched the official assembler
- `Wrong.asm`: has a duplicate label, to demonstrate the warning
- HDL files (CPU, Memory, Computer): add yours here
