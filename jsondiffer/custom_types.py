from typing import Dict, List, Tuple

from jsondiffer.diff_enum import DiffEnum

JsonType = Dict | List
PrimitiveDataType = str | bool | int | float | None
DiffKeyType = str | int
TokenType = Tuple[DiffKeyType]
DiffStoreType = Dict[TokenType, DiffEnum]
