from typing import Any, Callable, Dict, List
import json

from jsondiffer.custom_types import JsonType, DiffKeyType, PrimitiveDataType
from jsondiffer.diff_enum import DiffEnum
from jsondiffer.diff import Diff
from jsondiffer.tokenizer import Tokenizer


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
        self._diff_node(self.json_a, self.json_b, Tokenizer())
        print("Diffs generated:", self.diff_list)

    def _diff_node(
        self,
        json_a: JsonType | PrimitiveDataType,
        json_b: JsonType | PrimitiveDataType,
        tokenizer: Tokenizer,
    ):
        if self._is_mismatched(json_a, json_b):
            self.diff_list.append(Diff(DiffEnum.MISMATCHED, tokenizer.token()))
            return

        if isinstance(json_a, dict):
            longer_iterable: Dict[str, Any] = (
                json_b if len(json_a) < len(json_b) else json_a
            )
            for key in longer_iterable.keys():
                tokenizer.insert(key)
                if key not in json_a:
                    self.diff_list.append(
                        Diff(DiffEnum.MISSING_LEFT, tokenizer.token())
                    )
                    continue
                elif key not in json_b:
                    self.diff_list.append(
                        Diff(DiffEnum.MISSING_RIGHT, tokenizer.token())
                    )
                    continue
                self._diff_node(json_a[key], json_b[key], tokenizer)
                tokenizer.pop()
        elif isinstance(json_a, list):
            larger_len = len(json_b) if len(json_a) < len(json_b) else len(json_a)
            for idx in range(larger_len):
                tokenizer.insert(idx)
                if idx >= len(json_a):
                    self.diff_list.append(
                        Diff(DiffEnum.MISSING_LEFT, tokenizer.token())
                    )
                    continue
                elif idx >= len(json_b):
                    self.diff_list.append(
                        Diff(DiffEnum.MISSING_RIGHT, tokenizer.token())
                    )
                    continue
                self._diff_node(json_a[idx], json_b[idx], tokenizer)
                tokenizer.pop()
