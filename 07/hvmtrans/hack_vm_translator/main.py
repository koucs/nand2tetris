import argparse
import os
from hack_vm_translator.parser import Parser
from hack_vm_translator.code_writer import CodeWriter
from hack_vm_translator.constants import Command


def parse_args():
    parsed = argparse.ArgumentParser()
    parsed.add_argument('vm_file',
                        help='specify a hack vm file!')
    parsed.add_argument('--debug', help='output debug messages', action='store_true')
    return parsed.parse_known_args()


def main():
    args, unknown = parse_args()
    path = os.path.abspath(args.vm_file)
    p = Parser(path)
    in_name = os.path.basename(path)  # *.vm
    out_path = "{}/{}".format(os.path.dirname(path), os.path.splitext(in_name)[0] + ".asm")
    writer = CodeWriter(out_path, args.debug)

    while p.has_more_commands():
        p.advance()
        if p.command_type() in [Command.ARITHMETIC]:
            writer.write_arithmetic(p.command)
        elif p.command_type() in [Command.PUSH, Command.POP]:
            writer.write_push_pop(p.command_type(), p.arg1(), p.arg2())

        if args.debug:
            print("{:>3}: {:<20} {:<20} {:<20} {:<20}".format(
                p.index, p.command,
                str(p.command_type()),
                str(p.arg1()),
                str(p.arg2())
            ))

    writer.close()


if __name__ == '__main__':
    main()
