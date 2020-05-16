import xml.etree.ElementTree as ET
from jac.symbol_table import SymbolTable
from jac.constants import Kind


def _append_attrib(child, category, index, is_defined):
    child.attrib["category"] = category
    child.attrib["index"] = str(index)
    child.attrib["is_defined"] = str(is_defined)
    child.attrib["is_used"] = str(not is_defined)


class SymbolTableXml:

    def __init__(self, input_xml_path):
        self._tree = ET.parse(input_xml_path)
        self._st = SymbolTable()

    def analyze_symbol(self, debug):
        self._search_identifier(self._tree.getroot(), None, debug)
        return

    def _search_identifier(self, tree, parent_tag, debug):
        for i, child in enumerate(tree):
            if child.tag == "identifier":
                if debug:
                    print("{:<20}| {:<20}{:<10} | {:<20}{:<10}"
                          .format(str(parent_tag),
                                  str(tree[0].tag), str(tree[0].text),
                                  str(child.tag), str(child.text)))

                identifier = child.text

                if tree[0].text == " class ":
                    # Class category
                    _append_attrib(child, "class", 0, True)
                elif tree[0].text == " function ":
                    # Subroutine category
                    _append_attrib(child, "subroutine", 0, True)
                    self._st.start_subroutine()

                elif tree[0].text == " var " and i > 1:
                    # Var category
                    self._st.define(identifier, tree[1].text, Kind.VAR)
                    _append_attrib(child, "var", self._st.index_of(identifier), True)
                elif tree[0].text == " static " and i > 1:
                    # Var category
                    self._st.define(identifier, tree[1].text, Kind.STATIC)
                    _append_attrib(child, "static", self._st.index_of(identifier), True)
                elif tree[0].text == " field " and i > 1:
                    # Var category
                    self._st.define(identifier, tree[1].text, Kind.FIELD)
                    _append_attrib(child, "field", self._st.index_of(identifier), True)
                elif parent_tag == "parameterList" and i > 0:
                    # Var category
                    self._st.define(identifier, tree[i - 1].text, Kind.ARG)
                    _append_attrib(child, "arg", self._st.index_of(identifier), True)

                else:
                    _append_attrib(child, self._st.kind_of(identifier).name, self._st.index_of(identifier), False)

            if len(list(child)) != 0:
                self._search_identifier(list(child), child.tag, debug)
        return

    def write(self, output_xml_path):
        self._tree.write(output_xml_path)
        return
