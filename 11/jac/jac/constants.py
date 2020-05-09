from enum import Enum, auto

class Kind(Enum):
    STATIC = auto()
    FIELD = auto()
    ARG = auto()
    VAR = auto()
    NONE = auto()
