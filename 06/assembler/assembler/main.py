import argparse
import os
from parser import Parser
from asmcode import AsmCode
from symbol_table import SymbolTable
from constants import *
import pprint


def is_pos_int(s):
    try:
        val = int(s)
        return val >= 0
    except ValueError:
        return False


def parse_args():
    parsed = argparse.ArgumentParser()
    parsed.add_argument('asmfile', help='specify asm file!')
    return parsed.parse_known_args()


def main():
    args, unknown = parse_args()
    path = os.path.abspath(args.asmfile)

    # Initialize parser
    parser = Parser(path)
    code = AsmCode()
    table = SymbolTable()

    print("=== LOOP 1 : Create symbol table phase ===")

    index = 0
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() is Command.L:
            table.add_entry(parser.symbol(), index)
            index -= 1
        index += 1

    pprint.pprint(table.table())

    print("=== LOOP 2 output assembler phase ===")

    in_name = os.path.basename(path)  # *.asm
    f = open("{}/{}".format(os.path.dirname(path), os.path.splitext(in_name)[0] + ".hack"), "w")

    # Re-initialize parser
    parser = Parser(path)
    l_index = 16

    while parser.has_more_commands():
        parser.advance()
        # For debugging
        # print("{:>3}: {:<20}{:<20}{:<20}{:<20}{:<20}{:<20}".format(
        #     parser.index,
        #     parser.command,
        #     parser.command_type(),
        #     str(parser.symbol()),
        #     str(parser.dest()) + ": " + code.dest(parser.dest()),
        #     str(parser.comp()) + ": " + code.comp(parser.comp()),
        #     str(parser.jump()) + ": " + code.jump(parser.jump())
        # ))

        if parser.command_type() is Command.A:
            if is_pos_int(parser.symbol()):
                f.write("0" + str(bin(int(parser.symbol())))[2:].zfill(15) + '\n')
            else:
                if table.contains(parser.symbol()):
                    f.write(table.get_address(parser.symbol()) + '\n')
                else:
                    table.add_entry(parser.symbol(), l_index)
                    f.write(table.get_address(parser.symbol()) + '\n')
                    l_index += 1

        elif parser.command_type() is Command.C:
            f.write("111"
                    + code.comp(parser.comp())
                    + code.dest(parser.dest())
                    + code.jump(parser.jump()) + '\n')

    pprint.pprint(table.table())

    f.close()


if __name__ == '__main__':
    main()
