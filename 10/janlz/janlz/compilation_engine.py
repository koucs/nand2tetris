import xml.etree.ElementTree as ET

CLASS_VAR_DEC_KEYWORDS = ["static", "field"]
PARAMETER_LIST_TYPE_KEYWORDS = ["void", "int", "char"]


class CompilationEngine:
    def __init__(self, in_path, out_path):
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
        return

    def compile_class(self):
        self._dump_xml("<class>")
        self._indent += 1

        self._output("keyword", "class")
        self._output("identifier", None)
        self._output("symbol", "{")
        while self._text() in ["constructor", "function", "method", "static", "field"]:
            if self._text() in ["constructor", "function", "method"]:
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

        self._output("keyword", None)
        if self._text() in ["int", "char", "boolean"]:
            self._output("keyword", None)
        else:
            self._output("identifier", None)
        self._output("identifier", None)
        while self._text() == ",":
            self._output("symbol", ",")
            self._output("identifier", None)
        self._output("symbol", ";")

        self._indent -= 1
        self._dump_xml("</classVarDec>")
        return

    def compile_subroutine(self):
        self._dump_xml("<subroutineDec>")
        self._indent += 1

        self._output("keyword", None)
        if self._text() in ["void", "int", "char", "boolean"]:
            self._output("keyword", None)
        else:
            self._output("identifier", None)
        # subroutine name
        self._output("identifier", None)
        self._output("symbol", "(")
        self.compile_parameter_list()
        self._output("symbol", ")")
        self.compile_subroutine_body()

        self._indent -= 1
        self._dump_xml("</subroutineDec>")
        return

    def compile_subroutine_body(self):
        self._dump_xml("<subroutineBody>")
        self._indent += 1
        self._output("symbol", "{")

        while self._text() == "var":
            self.compile_var_dec()
        self.compile_statements()

        self._output("symbol", "}")
        self._indent -= 1
        self._dump_xml("</subroutineBody>")
        return

    VAR_TYPE_KEYWORDS = ["int", "char", "boolean"]

    def compile_parameter_list(self):
        self._dump_xml("<parameterList>")
        self._indent += 1

        if self._text() in self.VAR_TYPE_KEYWORDS:
            self._output("keyword", None)
            self._output("identifier", None)
        elif self._tag() == "identifier":
            self._output("identifier", None)
            self._output("identifier", None)

        while self._text() == ",":
            self._output("symbol", ",")
            if self._text() in self.VAR_TYPE_KEYWORDS:
                self._output("keyword", None)
                self._output("identifier", None)
            elif self._tag() == "identifier":
                self._output("identifier", None)
                self._output("identifier", None)
            else:
                break

        self._indent -= 1
        self._dump_xml("</parameterList>")
        return

    def compile_var_dec(self):
        self._dump_xml("<varDec>")
        self._indent += 1
        self._output("keyword", "var")

        if self._text() in self.VAR_TYPE_KEYWORDS:
            self._output("keyword", None)
        elif self._tag() == "identifier":
            self._output("identifier", None)

        while True:
            self._output("identifier", None)
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
        return

    def compile_while(self):
        self._dump_xml("<whileStatement>")
        self._indent += 1

        self._output("keyword", "while")
        self._output("symbol", "(")
        self.compile_expression()
        self._output("symbol", ")")
        self._output("symbol", "{")
        self.compile_statements()
        self._output("symbol", "}")

        self._indent -= 1
        self._dump_xml("</whileStatement>")
        return

    def compile_let(self):
        self._dump_xml("<letStatement>")
        self._indent += 1

        self._output("keyword", "let")
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
        return

    def compile_return(self):
        self._dump_xml("<returnStatement>")
        self._indent += 1

        self._output("keyword", "return")
        if self._text() != ";":
            self.compile_expression()
        self._output("symbol", ";")

        self._indent -= 1
        self._dump_xml("</returnStatement>")
        return

    def compile_if(self):
        self._dump_xml("<ifStatement>")
        self._indent += 1

        self._output("keyword", "if")
        self._output("symbol", "(")
        self.compile_expression()
        self._output("symbol", ")")

        self._output("symbol", "{")
        self.compile_statements()
        self._output("symbol", "}")

        if self._text() == "else":
            self._output("keyword", "else")
            self._output("symbol", "{")
            self.compile_statements()
            self._output("symbol", "}")

        self._indent -= 1
        self._dump_xml("</ifStatement>")
        return

    def compile_expression(self):
        self._dump_xml("<expression>")
        self._indent += 1

        self.compile_term()
        if self._text() in ["+", "-", "*", "/", "=", "&", "|", "<", ">"]:
            self._output("symbol", None)
            self.compile_term()

        self._indent -= 1
        self._dump_xml("</expression>")
        return

    def compile_term(self):
        self._dump_xml("<term>")
        self._indent += 1

        if self._tag() == "integerConstant":
            self._output("integerConstant", None)

        elif self._tag() == "stringConstant":
            self._output("stringConstant", None)

        elif self._tag() == "keyword" and self._text() in ["true", "false", "this", "null"]:
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
                self._output("identifier", None)


        elif self._tag() == "symbol" and self._text() == "(":
            self._output("symbol", "(")
            self.compile_expression()
            self._output("symbol", ")")

        elif self._tag() == "symbol" and self._text() in ["-", "~"]:
            self._output("symbol", None)
            self.compile_term()

        self._indent -= 1
        self._dump_xml("</term>")
        return

    def _compile_subroutine_call(self):
        self._output("identifier", None)
        if self._text() == "(":
            self._output("symbol", "(")
            self.compile_expression_list()
            self._output("symbol", ")")
        elif self._text() == ".":
            self._output("symbol", ".")
            self._output("identifier", None)
            self._output("symbol", "(")
            self.compile_expression_list()
            self._output("symbol", ")")
        return

    def compile_expression_list(self):
        self._dump_xml("<expressionList>")
        self._indent += 1

        # XXX: It seems a bad check condition...
        if self._text() != ")":
            self.compile_expression()
            while self._text() == ",":
                self._output("symbol", ",")
                self.compile_expression()

        self._indent -= 1
        self._dump_xml("</expressionList>")
        return

    PADDING = "  "

    def _dump_xml(self, string):
        self._out_file.write(self.PADDING * self._indent + string + "\n")

    def _output(self, tag, checked=None):
        e = self._element()
        if e.tag == tag and (checked is None or e.text == checked):
            append = ET.Element(tag)
            append.text = " {} ".format(e.text)
            xml_str = ET.tostring(append).decode()
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
