from enum import Enum


class DiffEnum(Enum):
    MISSING_LEFT = 1
    MISSING_RIGHT = 2
    MISMATCHED = 3
