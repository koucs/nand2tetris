from jac.constants import *


class SymbolTable:

    # static (class):  static PongGame instance; // the singelton, a Pong game instance
    # field (class):   field Bat bat;            // the bat
    # var (subroutine): var char key;
    # arg (subroutine): method void setDestination(int destx, int desty) {
    def __init__(self):
        self._class_scope_table = {e: [] for e in CLASS_SCOPE_KIND_LIST}
        self._subroutine_scope_table = {e: [] for e in SUBROUTINE_SCOPE_KIND_LIST}
        return

    def start_subroutine(self):
        self._subroutine_scope_table = {e: [] for e in SUBROUTINE_SCOPE_KIND_LIST}
        return

    def define(self, name, type, kind):
        self._get_table(kind).append({"name": name, "type": type})
        return

    def var_count(self, kind):
        return len(self._get_table(kind))

    def kind_of(self, name):
        kind, index, record = self._search_record(name)
        return kind

    def type_of(self, name):
        kind, index, record = self._search_record(name)
        if record is not {} and "type" in record.keys():
            return record["type"]

    def index_of(self, name):
        kind, index, record = self._search_record(name)
        return index

    def _get_table(self, kind):
        if kind in CLASS_SCOPE_KIND_LIST:
            return self._class_scope_table[kind]
        elif kind in SUBROUTINE_SCOPE_KIND_LIST:
            return self._subroutine_scope_table[kind]

    def _search_record(self, name):

        index = next((i for i, item in enumerate(self._get_table(Kind.VAR)) if item["name"] == name), None)
        if index is not None: return Kind.VAR, index, self._get_table(Kind.VAR)[index]

        index = next((i for i, item in enumerate(self._get_table(Kind.ARG)) if item["name"] == name), None)
        if index is not None: return Kind.ARG, index, self._get_table(Kind.ARG)[index]

        index = next((i for i, item in enumerate(self._get_table(Kind.FIELD)) if item["name"] == name), None)
        if index is not None: return Kind.FIELD, index, self._get_table(Kind.FIELD)[index]

        index = next((i for i, item in enumerate(self._get_table(Kind.STATIC)) if item["name"] == name), None)
        if index is not None: return Kind.STATIC, index, self._get_table(Kind.STATIC)[index]

        return Kind.NONE, None, {}
