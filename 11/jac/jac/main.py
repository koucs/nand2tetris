import argparse
import os
from janlz.tokenizer import Tokenizer
from janlz.compilation_engine import CompilationEngine
from jac.ex_compilation_engine import ExCompilationEngine
from janlz.main import tokenize
from jac.symbol_table_xml import SymbolTableXml


def parse_args():
    parsed = argparse.ArgumentParser()
    parsed.add_argument('jack_file',
                        help='specify a jack file '
                             'OR a directory containing one or more .jack source files!')
    parsed.add_argument('--debug', help='output debug messages', action='store_true')
    return parsed.parse_known_args()


def handle_input_file(args):
    path = os.path.abspath(args.jack_file)
    in_name = os.path.basename(path)  # *.vm
    out_T_path = "{}/output/{}".format(os.path.dirname(path), os.path.splitext(in_name)[0] + "T.xml")
    out_path = "{}/output/{}".format(os.path.dirname(path), os.path.splitext(in_name)[0] + ".xml")
    out_vm_path = "{}/output/{}".format(os.path.dirname(path), os.path.splitext(in_name)[0] + ".vm")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    output_xml(path, out_T_path, out_path, out_vm_path, args.debug)


def handle_input_dir(args):
    abs_in_path = os.path.abspath(args.jack_file)  # ../dir -> /path/to/dir
    abs_out_dir_path = "{}/output/".format(abs_in_path)  # /path/to/dir/output/
    os.makedirs(os.path.dirname(abs_out_dir_path), exist_ok=True)
    jack_paths = [os.path.join(abs_in_path, f) for f in os.listdir(abs_in_path) if f.endswith(".jack")]

    for path in jack_paths:
        out_T_path = "{}{}T.xml".format(abs_out_dir_path, os.path.basename(os.path.splitext(path)[0]))
        out_path = "{}{}.xml".format(abs_out_dir_path, os.path.basename(os.path.splitext(path)[0]))
        out_vm_path = "{}{}.vm".format(abs_out_dir_path, os.path.basename(os.path.splitext(path)[0]))
        output_xml(path, out_T_path, out_path, out_vm_path, args.debug)
    return


def output_xml(jack_path, t_xml_path, c_xml_path, vm_path, debug):
    if debug:
        print("{:<25}: {}\n{:<25}: {}\n{:<25}: {}\n{:<25}: {}\n".format("input", jack_path,
                                                                        "output (tokenized)", t_xml_path,
                                                                        "output (parsed)", c_xml_path,
                                                                        "output (vm)", vm_path))

    # Chapter 10: Tokenizer
    f = open(t_xml_path, "w")
    t = Tokenizer(jack_path)
    tokenize(t, f, False)
    f.close()

    # Chapter 11: Expanded Compilation Engine
    c = ExCompilationEngine(t_xml_path, c_xml_path, vm_path)
    c.compile_class()
    c.close()

    # Chapter 11: Symbol Table
    # stf = SymbolTableXml(c_xml_path)
    # stf.analyze_symbol(debug)
    # stf.write(st_xml_path)


def main():
    args, unknown = parse_args()
    if os.path.isfile(args.jack_file):
        handle_input_file(args)
    elif os.path.isdir(args.jack_file):
        handle_input_dir(args)
    else:
        print("Unexpected input a file or a directory path.")


if __name__ == '__main__':
    main()
