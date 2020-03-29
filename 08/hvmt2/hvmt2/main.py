import argparse
import os
from hvmt2.parser import Parser
from hvmt2.code_writer import CodeWriter
from hvmt2.constants import Command


def parse_args():
    parsed = argparse.ArgumentParser()
    parsed.add_argument('vm_file',
                        help='specify a hack vm file '
                             'OR a directory containing one or more .vm source files!')
    parsed.add_argument('--debug', help='output debug messages', action='store_true')
    return parsed.parse_known_args()


def translate(p, w, debug):
    while p.has_more_commands():
        p.advance()

        if p.command_type() in [Command.ARITHMETIC]:
            w.write_arithmetic(p.command)
        elif p.command_type() in [Command.PUSH, Command.POP]:
            w.write_push_pop(p.command_type(), p.arg1(), p.arg2())
        elif p.command_type() is Command.LABEL:
            w.write_label(p.arg1())
        elif p.command_type() is Command.IF:
            w.write_if(p.arg1())
        elif p.command_type() is Command.GOTO:
            w.write_goto(p.arg1())
        elif p.command_type() is Command.CALL:
            w.write_call(p.arg1(), p.arg2())
        elif p.command_type() is Command.FUNCTION:
            w.write_function(p.arg1(), p.arg2())
        elif p.command_type() is Command.RETURN:
            w.write_return()

        if debug:
            print("{:>3}: {:<30} {:<20} {:<20} {:<10}".format(
                p.index, p.command,
                str(p.command_type()),
                str(p.arg1()),
                str(p.arg2())
            ))
    return


def handle_input_file(args):
    path = os.path.abspath(args.vm_file)
    in_name = os.path.basename(path)  # *.vm
    out_path = "{}/{}".format(os.path.dirname(path), os.path.splitext(in_name)[0] + ".asm")
    w = CodeWriter(out_path, args.debug)
    p = Parser(path)
    translate(p, w, args.debug)
    w.close()
    return


def handle_input_dir(args):
    abs_in_path = os.path.abspath(args.vm_file)  # ../dir -> /path/to/dir
    abs_out_basename = os.path.basename(abs_in_path)  # /path/to/dir -> dir
    out_path = "{}/{}".format(abs_in_path, abs_out_basename + ".asm")  # /path/to/dir/dir.asm
    vm_paths = [os.path.join(abs_in_path, f) for f in os.listdir(abs_in_path) if f.endswith(".vm")]
    print(vm_paths)

    w = CodeWriter(out_path, args.debug)

    # bootstrap code
    w.set_file_name("BOOTSTRAP")
    w.write_init()

    for path in vm_paths:
        p = Parser(path)
        w.set_file_name(os.path.basename(os.path.splitext(path)[0]))  # for the return-address
        translate(p, w, args.debug)
    w.close()


def main():
    args, unknown = parse_args()
    if os.path.isfile(args.vm_file):
        handle_input_file(args)
    elif os.path.isdir(args.vm_file):
        handle_input_dir(args)
    else:
        print("Unexpected input a file or a directory path.")


if __name__ == '__main__':
    main()
