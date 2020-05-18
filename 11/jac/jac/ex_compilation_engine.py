import xml.etree.ElementTree as ET
from jac.symbol_table import SymbolTable
from jac.constants import *
from jac.vm_writer import VMWriter

CLASS_VAR_DEC_KEYWORDS = ["static", "field"]
PARAMETER_LIST_TYPE_KEYWORDS = ["void", "int", "char"]


class ExCompilationEngine:
    def __init__(self, in_path, out_path, out_vm_path):
        self._in_path = in_path
        self._in_path = out_path
        self._out_file = open(out_path, "w")

        self._indent = 0
        xml_input = ""
        with open(in_path) as f:
            # remove whitespaces from a input XML file.
            for line in f:
                # XXX: For avoiding a bad whitespace's replacement.
                # NG: <stringConstant> HOW MANY ~!  </stringConstant> => <stringConstant>HOWMANY~</stringConstant>
                # NG: <stringConstant> HOW MANY ~!  </stringConstant> => <stringConstant>HOW MANY ~! </stringConstant>
                if line.startswith("<stringConstant>"):
                    xml_input += line.strip() \
                        .replace("<stringConstant> ", "<stringConstant>") \
                        .replace(" </stringConstant>", "</stringConstant>")
                else:
                    xml_input += line.strip().replace(" ", "")

        # tree = ET.parse(xml_input)
        # self._root = tree.getroot()
        self._root = ET.fromstring(xml_input)
        if self._root.tag != "tokens":
            raise RuntimeError("The root tag should be '<tokens>~</tokens>'.")
        self._line_num = 0

        self._symbol_table = SymbolTable()
        self._vm_writer = VMWriter(out_vm_path)

        self._class_name = None
        self._subroutine_params_num = 0
        self._expression_num = 0
        self._var_dec_num = 0
        self._class_dec_num = 0
        self._subroutine_name = ""
        self._if_count = 0
        self._while_count = 0
        return

    def close(self):
        self._out_file.close()
        self._vm_writer.close()
        return

    def compile_class(self):
        self._dump_xml("<class>")
        self._indent += 1

        self._output("keyword", "class")
        self._class_name = self._text()

        self._output("identifier", None)
        self._output("symbol", "{")

        while self._text() in ["constructor", "function", "method", "static", "field"]:
            if self._text() in ["constructor", "function", "method"]:
                self._subroutine_type = self._text()
                self.compile_subroutine()
            elif self._text() in ["static", "field"]:
                self.compile_class_var_dec()
        self._output("symbol", "}")

        self._indent -= 1
        self._dump_xml("</class>")
        return

    def compile_class_var_dec(self):
        self._dump_xml("<classVarDec>")
        self._indent += 1

        category_kind = Kind.STATIC if self._text() == "static" else Kind.FIELD

        self._output("keyword", None)

        type = self._text()
        if self._text() in ["int", "char", "boolean"]:
            self._output("keyword", None)
        else:
            self._output("identifier", None)

        self._symbol_table.define(self._text(), type, category_kind)
        self._output("identifier", None)
        self._class_dec_num += 1

        while self._text() == ",":
            self._output("symbol", ",")
            self._symbol_table.define(self._text(), type, category_kind)
            self._output("identifier", None)
            self._class_dec_num += 1
        self._output("symbol", ";")

        self._indent -= 1
        self._dump_xml("</classVarDec>")
        return

    def compile_subroutine(self):

        self._symbol_table.start_subroutine()

        self._dump_xml("<subroutineDec>")
        self._indent += 1

        self._output("keyword", None)
        if self._text() in ["void", "int", "char", "boolean"]:
            self._output("keyword", None)
        else:
            self._output("identifier", None)
        # subroutine name
        self._subroutine_name = self._text()
        self._output("identifier", None)
        self._output("symbol", "(")

        self._subroutine_params_num = 0
        self.compile_parameter_list()

        self._if_count = 0
        self._while_count = 0
        self._output("symbol", ")")
        self.compile_subroutine_body()

        self._indent -= 1
        self._dump_xml("</subroutineDec>")

        return

    def compile_subroutine_body(self):
        self._dump_xml("<subroutineBody>")
        self._indent += 1
        self._output("symbol", "{")

        self._var_dec_num = 0
        while self._text() == "var":
            self.compile_var_dec()

        self._vm_writer.write_function("{}.{}".format(self._class_name, self._subroutine_name), self._var_dec_num)
        if self._subroutine_type == "constructor":
            self._vm_writer.write_push("constant", self._class_dec_num)
            self._vm_writer.write_call("Memory.alloc", 1)
            self._vm_writer.write_pop("pointer", 0)
        elif self._subroutine_type == "method":
            self._vm_writer.write_push("argument", 0)
            self._vm_writer.write_pop("pointer", 0)

        self.compile_statements()

        self._output("symbol", "}")
        self._indent -= 1
        self._dump_xml("</subroutineBody>")
        return

    VAR_TYPE_KEYWORDS = ["int", "char", "boolean"]

    def compile_parameter_list(self):
        self._dump_xml("<parameterList>")
        self._indent += 1

        type = self._text()
        if self._text() in self.VAR_TYPE_KEYWORDS:
            self._output("keyword", None)
            self._symbol_table.define(self._text(), type, Kind.ARG)
            self._output("identifier", None)
            self._subroutine_params_num += 1
        elif self._tag() == "identifier":
            self._output("identifier", None)
            self._symbol_table.define(self._text(), type, Kind.ARG)
            self._output("identifier", None)
            self._subroutine_params_num += 1

        while self._text() == ",":
            type = self._text()
            self._output("symbol", ",")
            if self._text() in self.VAR_TYPE_KEYWORDS:
                self._output("keyword", None)
                self._symbol_table.define(self._text(), type, Kind.ARG)
                self._output("identifier", None)
                self._subroutine_params_num += 1
            elif self._tag() == "identifier":
                self._output("identifier", None)
                self._symbol_table.define(self._text(), type, Kind.ARG)
                self._output("identifier", None)
                self._subroutine_params_num += 1
            else:
                break

        self._indent -= 1
        self._dump_xml("</parameterList>")
        return

    def compile_var_dec(self):
        self._dump_xml("<varDec>")
        self._indent += 1
        self._output("keyword", "var")

        type = self._text()
        if self._text() in self.VAR_TYPE_KEYWORDS:
            self._output("keyword", None)
        elif self._tag() == "identifier":
            self._output("identifier", None)

        while True:
            self._symbol_table.define(self._text(), type, Kind.VAR)
            self._output("identifier", None)
            self._var_dec_num += 1
            if self._text() == ",":
                self._output("symbol", ",")
            else:
                break

        self._output("symbol", ";")
        self._indent -= 1
        self._dump_xml("</varDec>")
        return

    def _var_type(self):
        if self._text() in self.VAR_TYPE_KEYWORDS:
            self._output("keyword", None)
            self._output("identifier", None)
        elif self._tag() == "identifier":
            self._output("identifier", None)
            self._output("identifier", None)
        return

    def compile_statements(self):
        self._dump_xml("<statements>")
        self._indent += 1

        while self._text() in ["let", "if", "while", "do", "return"]:
            if self._text() == "if":
                self.compile_if()
            elif self._text() == "let":
                self.compile_let()
            elif self._text() == "while":
                self.compile_while()
            elif self._text() == "do":
                self.compile_do()
            else:
                self.compile_return()

        self._indent -= 1
        self._dump_xml("</statements>")
        return

    def compile_do(self):
        self._dump_xml("<doStatement>")
        self._indent += 1

        self._output("keyword", "do")
        self._compile_subroutine_call()
        self._output("symbol", ";")

        self._indent -= 1
        self._dump_xml("</doStatement>")
        self._vm_writer.write_pop("temp", 0)
        return

    def compile_while(self):
        self._dump_xml("<whileStatement>")
        self._indent += 1
        label_exp = "WHILE_EXP" + str(self._while_count)
        label_end = "WHILE_END" + str(self._while_count)
        self._while_count += 1

        self._output("keyword", "while")
        self._vm_writer.write_label(label_exp)

        self._output("symbol", "(")
        self.compile_expression()
        self._output("symbol", ")")
        self._output("symbol", "{")

        self._vm_writer.write_arithmetic("not")
        self._vm_writer.write_if(label_end)

        self.compile_statements()
        self._output("symbol", "}")

        self._indent -= 1
        self._dump_xml("</whileStatement>")

        self._vm_writer.write_goto(label_exp)
        self._vm_writer.write_label(label_end)
        return

    def compile_let(self):
        self._dump_xml("<letStatement>")
        self._indent += 1

        self._output("keyword", "let")
        let_identifier = self._text()
        self._output("identifier", None)

        if self._text() == "[":
            self._output("symbol", "[")
            self.compile_expression()
            self._output("symbol", "]")

        self._output("symbol", "=")
        self.compile_expression()
        self._output("symbol", ";")

        self._indent -= 1
        self._dump_xml("</letStatement>")

        self._vm_writer.write_pop(KIND_VM_MAP.get(self._symbol_table.kind_of(let_identifier)),
                                  self._symbol_table.index_of(let_identifier))
        return

    def compile_return(self):
        self._dump_xml("<returnStatement>")
        self._indent += 1

        self._output("keyword", "return")
        if self._text() != ";":
            self.compile_expression()
        else:
            self._vm_writer.write_push("constant", 0)
        self._output("symbol", ";")
        self._vm_writer.write_return()

        self._indent -= 1
        self._dump_xml("</returnStatement>")
        return

    def compile_if(self):
        self._dump_xml("<ifStatement>")
        self._indent += 1

        true_label = "IF_TRUE" + str(self._if_count)
        false_label = "IF_FALSE" + str(self._if_count)
        end_label = "IF_END" + str(self._if_count)
        # this count should be counted-up after making these labels immediately
        self._if_count += 1

        self._output("keyword", "if")
        self._output("symbol", "(")
        self.compile_expression()
        self._output("symbol", ")")

        self._vm_writer.write_if(true_label)
        self._vm_writer.write_goto(false_label)
        self._vm_writer.write_label(true_label)

        self._output("symbol", "{")
        self.compile_statements()
        self._output("symbol", "}")

        if self._text() == "else":
            self._vm_writer.write_goto(end_label)
            self._vm_writer.write_label(false_label)

            self._output("keyword", "else")
            self._output("symbol", "{")
            self.compile_statements()
            self._output("symbol", "}")

            self._vm_writer.write_label(end_label)
        else:
            self._vm_writer.write_label(false_label)

        self._indent -= 1
        self._dump_xml("</ifStatement>")

        return

    def compile_expression(self):
        self._dump_xml("<expression>")
        self._indent += 1

        command = None

        self.compile_term()
        if self._text() in ["+", "-", "*", "/", "=", "&", "|", "<", ">"]:

            if self._text() == "+":
                command = "add"
            elif self._text() == "-":
                command = "sub"
            elif self._text() == "*":
                command = "call Math.multiply 2"
            elif self._text() == "/":
                command = "call Math.divide 2"
            elif self._text() == ">":
                command = "gt"
            elif self._text() == "<":
                command = "lt"
            elif self._text() == "&":
                command = "and"
            elif self._text() == "=":
                command = "eq"

            self._output("symbol", None)
            self.compile_term()

        if command is not None: self._vm_writer.write_arithmetic(command)

        self._indent -= 1
        self._dump_xml("</expression>")
        return

    def compile_term(self):
        self._dump_xml("<term>")
        self._indent += 1

        if self._tag() == "integerConstant":
            self._vm_writer.write_push("constant", int(self._text()))
            self._output("integerConstant", None)

        elif self._tag() == "stringConstant":
            self._output("stringConstant", None)

        elif self._tag() == "keyword" and self._text() in ["true", "false", "this", "null"]:
            if self._text() == "true":
                self._vm_writer.write_push("constant", 0)
                self._vm_writer.write_arithmetic("not")
            elif self._text() == "false":
                self._vm_writer.write_push("constant", 0)
            elif self._text() == "this":
                self._vm_writer.write_push("pointer", 0)
            self._output("keyword", None)

        elif self._tag() == "identifier":
            # fetch a advanced element.
            next_element = self._root[self._line_num + 1]

            if next_element.text == "[":
                self._output("identifier", None)
                self._output("symbol", "[")
                self.compile_expression()
                self._output("symbol", "]")

            elif next_element.text in ["(", "."]:
                self._compile_subroutine_call()

            else:
                self._vm_writer.write_push(KIND_VM_MAP.get(self._symbol_table.kind_of(self._text())),
                                           self._symbol_table.index_of(self._text()))
                self._output("identifier", None)


        elif self._tag() == "symbol" and self._text() == "(":
            self._output("symbol", "(")
            self.compile_expression()
            self._output("symbol", ")")

        elif self._tag() == "symbol" and self._text() in ["-", "~"]:
            unary_operator = self._text()
            self._output("symbol", None)
            self.compile_term()
            if unary_operator == "-":
                self._vm_writer.write_arithmetic("neg")
            else:
                self._vm_writer.write_arithmetic("not")

        self._indent -= 1
        self._dump_xml("</term>")
        return

    def _compile_subroutine_call(self):

        self._expression_num = 0

        method = self._text()

        # The case of new method
        if (self._symbol_table.kind_of(method) != Kind.NONE):
            instance_name = method
            method = self._symbol_table.type_of(method)
            self._expression_num += 1
            self._vm_writer.write_push(KIND_VM_MAP.get(self._symbol_table.kind_of(instance_name)),
                                       self._symbol_table.index_of(instance_name))

        self._output("identifier", None)

        if self._text() == "(":
            method = self._class_name + "." + method
            self._expression_num += 1
            self._output("symbol", "(")
            self.compile_expression_list()
            self._output("symbol", ")")
            self._vm_writer.write_push("pointer", 0)
        elif self._text() == ".":
            self._output("symbol", ".")
            method += "." + self._text()
            self._output("identifier", None)
            self._output("symbol", "(")
            self.compile_expression_list()
            self._output("symbol", ")")

        self._vm_writer.write_call(method, self._expression_num)
        return

    def compile_expression_list(self):
        self._dump_xml("<expressionList>")
        self._indent += 1

        # XXX: It seems a bad check condition...
        if self._text() != ")":
            self.compile_expression()
            self._expression_num += 1
            while self._text() == ",":
                self._output("symbol", ",")
                self.compile_expression()
                self._expression_num += 1

        self._indent -= 1
        self._dump_xml("</expressionList>")
        return

    PADDING = "  "

    def _dump_xml(self, string):
        self._out_file.write(self.PADDING * self._indent + string + "\n")

    def _output(self, tag, checked=None):
        e = self._element()
        if e.tag == tag and (checked is None or e.text == checked):
            elem = ET.Element(tag)
            elem.text = " {} ".format(e.text)
            xml_str = ET.tostring(elem).decode()
            self._dump_xml(xml_str)
        # else:
        #     raise RuntimeError("Compile Error")
        self._advance()

    def _output_identifier(self, category, index, is_defined):
        e = self._element()
        if e.tag == "identifier":
            elem = ET.Element("identifier")
            elem.text = " {} ".format(e.text)
            xml_str = ET.tostring(elem).decode()
            self._dump_xml(xml_str)
        # else:
        #     raise RuntimeError("Compile Error")
        self._advance()

    def _element(self):
        return self._root[self._line_num]

    def _tag(self):
        return self._root[self._line_num].tag

    def _text(self):
        return self._root[self._line_num].text

    def _advance(self):
        self._line_num += 1
        return
