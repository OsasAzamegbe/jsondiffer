from datetime import datetime
from typing import Callable, Dict, List
from dataclasses import dataclass
from enum import Enum
import json
from unittest.mock import NonCallableMagicMock


JsonType = Dict | List
PrimitiveDataType = str | bool | int | float | None
DiffKeyType = str | int | None


class DiffEnum(Enum):
    MISSING_LEFT = 1
    MISSING_RIGHT = 2
    MISMATCHED = 3


@dataclass
class Diff(object):
    diff_type: DiffEnum
    key: DiffKeyType


class JsonDiffer(object):
    def __init__(self, json_a: JsonType = None, json_b: JsonType = None) -> None:
        self.json_a = json_a if json_a is not None else {}
        self.json_b = json_b if json_b is not None else {}
        self.diff_list: List[Diff] = []

    @staticmethod
    def _is_json_loadable(
        load_function: Callable, json_data: str, *args, **kwargs
    ) -> bool:
        try:
            load_function(json_data, *args, **kwargs)
        except ValueError:
            return False
        return True

    @staticmethod
    def is_valid_json(json_data: str, is_file: bool = False) -> bool:
        if is_file:
            with open(json_data, "r") as json_file:
                return JsonDiffer._is_json_loadable(json.load, json_file)
        return JsonDiffer._is_json_loadable(json.loads, json_data)

    @staticmethod
    def _is_mismatched(
        json_a: JsonType | PrimitiveDataType,
        json_b: JsonType | PrimitiveDataType,
    ) -> bool:
        return type(json_a) is not type(json_b) or (
            isinstance(json_a, PrimitiveDataType) and json_a != json_b
        )

    def generate_diffs(self):
        self._diff_node(self.json_a, self.json_b)
        print("Diffs generated:", self.diff_list)

    def _diff_node(
        self,
        json_a: JsonType | PrimitiveDataType,
        json_b: JsonType | PrimitiveDataType,
        prev_key: DiffKeyType = None,
    ):
        if self._is_mismatched(json_a, json_b):
            self.diff_list.append(Diff(DiffEnum.MISMATCHED, prev_key))
            return

        if isinstance(json_a, dict):
            longer_iterable = json_b if len(json_a) < len(json_b) else json_a
            for key in longer_iterable.keys():
                if key not in json_a:
                    self.diff_list.append(Diff(DiffEnum.MISSING_LEFT, key))
                    continue
                elif key not in json_b:
                    self.diff_list.append(Diff(DiffEnum.MISSING_RIGHT, key))
                    continue
                self._diff_node(json_a[key], json_b[key], key)
        elif isinstance(json_a, list):
            larger_len = len(json_b) if len(json_a) < len(json_b) else len(json_a)
            for idx in range(larger_len):
                if idx >= len(json_a):
                    self.diff_list.append(Diff(DiffEnum.MISSING_LEFT, idx))
                    continue
                elif idx >= len(json_b):
                    self.diff_list.append(Diff(DiffEnum.MISSING_RIGHT, idx))
                    continue
                self._diff_node(json_a[idx], json_b[idx], idx)
