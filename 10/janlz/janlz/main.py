import argparse
import os
from janlz.tokenizer import Tokenizer
from janlz.constants import Token, ESCAPED_SYMBOL


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
    out_path = "{}/output/{}".format(os.path.dirname(path), os.path.splitext(in_name)[0] + "T.xml")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    out = open(out_path, "w")
    t = Tokenizer(path)
    tokenize(t, out, args.debug)
    out.close()


def handle_input_dir(args):
    abs_in_path = os.path.abspath(args.jack_file)  # ../dir -> /path/to/dir
    abs_out_dir_path = "{}/output/".format(abs_in_path)  # /path/to/dir/output/l
    os.makedirs(os.path.dirname(abs_out_dir_path), exist_ok=True)
    jack_paths = [os.path.join(abs_in_path, f) for f in os.listdir(abs_in_path) if f.endswith(".jack")]

    for path in jack_paths:
        out_xml_path = "{}{}T.xml".format(abs_out_dir_path, os.path.basename(os.path.splitext(path)[0]))
        if args.debug:
            print("in : {}\nout: {}\n".format(path, out_xml_path))

        out = open(out_xml_path, "w")
        t = Tokenizer(path)
        tokenize(t, out, args.debug)
        out.close()

    return


def tokenize(t, f, debug):
    f.write("<tokens>\n")
    while t.has_more_token():
        t.advance()
        if debug:
            print("{:>3}: {:<30} {:<20} {:<20} {:<10} {:<20} {:<10} {:<10}".format(
                t.index, t.line[0:10],
                str(t.token_type()),
                str(t.keyword()),
                str(t.symbol()),
                str(t.identifier()),
                str(t.int_val()),
                str(t.string_val())
            ))

        if t.token_type() is Token.KEYWORD:
            f.write("<keyword> {0} </keyword>\n".format(t.keyword().name.lower()))
        elif t.token_type() is Token.SYMBOL:
            f.write("<symbol> {0} </symbol>\n".format(ESCAPED_SYMBOL.get(t.symbol(), t.symbol())))
        elif t.token_type() is Token.IDENTIFIER:
            f.write("<identifier> {0} </identifier>\n".format(t.identifier()))
        elif t.token_type() is Token.STRING_CONST:
            f.write("<stringConstant> {0} </stringConstant>\n".format(t.string_val()))
        elif t.token_type() is Token.INT_CONST:
            f.write("<integerConstant> {0} </integerConstant>\n".format(t.int_val()))

    f.write("</tokens>\n")
    return


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
