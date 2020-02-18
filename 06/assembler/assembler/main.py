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
    while parser.has_more_commands():
        parser.advance()
        print("{}: {}".format(parser.index, parser.command))


if __name__ == '__main__':
    main()
