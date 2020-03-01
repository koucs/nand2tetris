import argparse
import os
from hack_vm_translator.parser import Parser


def parse_args():
    parsed = argparse.ArgumentParser()
    parsed.add_argument('vm_file',
                        help='specify a hack vm file!')
    parsed.add_argument('--debug', help='output debug messages', action='store_true')
    return parsed.parse_known_args()


def main():
    args, unknown = parse_args()
    path = os.path.abspath(args.vm_file)
    print(path)

    parser = Parser(path)
    while parser.has_more_commands():
        parser.advance()
        if args.debug:
            print("{:>3}: {:<20} {:<20} {:<20} {:<20}".format(
                parser.index,
                parser.command,
                str(parser.command_type()),
                str(parser.arg1()),
                str(parser.arg2())
            ))

    in_name = os.path.basename(path)  # *.vm
    f = open("{}/{}".format(
        os.path.dirname(path),
        os.path.splitext(in_name)[0] + ".asm"),
        "w")

    f.close()


if __name__ == '__main__':
    main()
