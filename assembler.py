#!/usr/bin/env python3
"""Hack assembler: .asm -> .hack
Usage: python assembler.py Prog.asm [K]
Extra feature chosen by K mod 3 (0: symbols.txt, 1: error messages, 2: duplicate-label warning).
Error messages and duplicate warnings are cheap, so they run for every K; symbols.txt
is written only when K mod 3 == 0 (or K is omitted).
"""
import sys

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100",
    "A": "0110000", "!D": "0001101", "!A": "0110001", "-D": "0001111",
    "-A": "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011", "A-D": "0000111",
    "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
}
DEST = {"": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}


def predefined():
    t = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
         "SCREEN": 16384, "KBD": 24576}
    for i in range(16):
        t["R%d" % i] = i
    return t


def clean(line):
    return line.split("//")[0].replace(" ", "").replace("\t", "").strip()


def is_symbol(s):
    return s != "" and not s[0].isdigit() and all(c.isalnum() or c in "_.$:" for c in s)


def assemble(path, k=None):
    with open(path) as f:
        raw = f.read().splitlines()

    symbols = predefined()
    labels = {}
    errors, warnings = [], []
    instrs = []          # (line_number, text)

    # ---------- First reading: strip comments/blanks, record labels ----------
    for n, line in enumerate(raw, 1):
        s = clean(line)
        if not s:
            continue
        if s.startswith("("):
            if not s.endswith(")") or not is_symbol(s[1:-1]):
                errors.append("Line %d: invalid label '%s'" % (n, s))
                continue
            name = s[1:-1]
            if name in labels:
                warnings.append("Warning line %d: label '%s' already defined (first at ROM %d)"
                                % (n, name, labels[name]))
                continue
            labels[name] = len(instrs)
            symbols[name] = len(instrs)
        else:
            instrs.append((n, s))

    # ---------- Second reading: translate ----------
    out = []
    next_var = 16
    variables = {}
    for n, s in instrs:
        if s[0] == "@":
            sym = s[1:]
            if sym.isdigit():
                val = int(sym)
                if val > 32767:
                    errors.append("Line %d: address %d too large (max 32767)" % (n, val))
                    continue
            elif is_symbol(sym):
                if sym not in symbols:
                    symbols[sym] = next_var
                    variables[sym] = next_var
                    next_var += 1
                val = symbols[sym]
            else:
                errors.append("Line %d: invalid instruction '%s'" % (n, s))
                continue
            out.append(format(val, "016b"))
        else:
            dest, jump = "", ""
            body = s
            if ";" in body:
                body, jump = body.split(";", 1)
            if "=" in body:
                dest, body = body.split("=", 1)
            comp = body
            if comp not in COMP or dest not in DEST or jump not in JUMP:
                errors.append("Line %d: invalid instruction '%s'" % (n, s))
                continue
            out.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])

    for w in warnings:
        print(w)
    if errors:
        for e in errors:
            print(e)
        print("Assembly failed: %d error(s). No .hack file written." % len(errors))
        sys.exit(1)

    outpath = path.rsplit(".", 1)[0] + ".hack"
    with open(outpath, "w") as f:
        f.write("\n".join(out) + "\n")
    print("Wrote %s (%d instructions)" % (outpath, len(out)))

    if k is None or k % 3 == 0:
        with open("symbols.txt", "w") as f:
            f.write("LABELS\n")
            for name, addr in labels.items():
                f.write("%s\t%d\n" % (name, addr))
            f.write("VARIABLES\n")
            for name, addr in variables.items():
                f.write("%s\t%d\n" % (name, addr))
        print("Wrote symbols.txt")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py Prog.asm [K]")
        sys.exit(1)
    assemble(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None)
