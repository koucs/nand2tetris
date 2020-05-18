from enum import Enum, auto


class Kind(Enum):
    STATIC = auto()
    FIELD = auto()
    ARG = auto()
    VAR = auto()
    NONE = auto()


CLASS_SCOPE_KIND_LIST = [Kind.STATIC, Kind.FIELD]

SUBROUTINE_SCOPE_KIND_LIST = [Kind.ARG, Kind.VAR]

KIND_VM_MAP = {
    Kind.ARG: "argument",
    Kind.VAR: "local",
    Kind.STATIC: "static",
    Kind.FIELD: "this",
    Kind.NONE: "NONE"
}