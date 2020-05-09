from enum import Enum, auto


class Kind(Enum):
    STATIC = auto()
    FIELD = auto()
    ARG = auto()
    VAR = auto()
    NONE = auto()


CLASS_SCOPE_KIND_LIST = [Kind.STATIC, Kind.FIELD]

CLASS_SCOPE_KIND_LOOKUP_DICT = {
    Kind.STATIC.name.lower(): Kind.STATIC,
    Kind.FIELD.name.lower(): Kind.FIELD
}

SUBROUTINE_SCOPE_KIND_LIST = [Kind.ARG, Kind.VAR]

SUBROUTINE_SCOPE_KIND_LOOKUP_DICT = {
    Kind.ARG.name.lower(): Kind.ARG,
    Kind.VAR.name.lower(): Kind.VAR
}
