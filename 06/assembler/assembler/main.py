import argparse
import os
from parser import Parser


def parse_args():
    parsed = argparse.ArgumentParser()
    parsed.add_argument('asmfile', help='specify asm file!')
    return parsed.parse_known_args()


def main():
    args, unknown = parse_args()
    path = os.path.abspath(args.asmfile)
    parser = Parser(path)

    in_dir = os.path.dirname(path)  # path/to
    in_name = os.path.basename(path)  # *.asm
    out_name = os.path.splitext(in_name)[0] + ".hack"  # *.hack

    while parser.has_more_commands():
        parser.advance()
        print("{}: {} {}".format(parser.index, parser.command, parser.command_type()))


if __name__ == '__main__':
    main()
