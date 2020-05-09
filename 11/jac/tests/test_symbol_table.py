from jac.symbol_table import SymbolTable
from jac.constants import *


def _prepare(table):
    table.define("static1", "string", Kind.STATIC)
    table.define("static2", "int", Kind.STATIC)
    table.define("static3", "string", Kind.STATIC)
    table.define("static4", "boolean", Kind.STATIC)
    table.define("static5", "string", Kind.STATIC)

    table.define("field1", "string", Kind.FIELD)
    table.define("field2", "int", Kind.FIELD)
    table.define("field3", "int", Kind.FIELD)
    table.define("field4", "int", Kind.FIELD)

    table.define("var1", "string", Kind.VAR)
    table.define("var2", "int", Kind.VAR)
    table.define("var3", "int", Kind.VAR)

    table.define("arg1", "string", Kind.ARG)
    table.define("arg2", "int", Kind.ARG)
    return


def test_define():
    ## Given
    table = SymbolTable()

    ## When
    _prepare(table)

    ## Then
    assert table.index_of("arg1") == 0
    assert table.kind_of("arg2") == Kind.ARG
    assert table.type_of("arg2") == "int"
    assert table.var_count(Kind.ARG) == 2

    assert table.index_of("field1") == 0
    assert table.kind_of("var3") == Kind.VAR
    assert table.type_of("static5") == "string"

    assert table.index_of("not_exists") == None
    assert table.kind_of("not_exists") == Kind.NONE
    assert table.type_of("not_exists") == None


def test_start_subroutine():
    ## Given
    table = SymbolTable()
    _prepare(table)

    ## When
    table.start_subroutine()

    ## Then
    assert table.var_count(Kind.ARG) == 0
    assert table.index_of("arg1") == None
    assert table.kind_of("arg2") == Kind.NONE
    assert table.type_of("arg2") == None
    assert table.kind_of("var3") == Kind.NONE

    assert table.index_of("field1") == 0
    assert table.type_of("static5") == "string"
