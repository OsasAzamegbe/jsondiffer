from typing import Any, Callable, Dict
import json

from jsondiffer.custom_types import DffStoreType, JsonType, PrimitiveDataType
from jsondiffer.diff_enum import DiffEnum
from jsondiffer.diff_printer import DiffPrinter
from jsondiffer.tokenizer import Tokenizer


class JsonDiffer(object):
    def __init__(self, json_a: JsonType, json_b: JsonType, diff_printer: DiffPrinter = None) -> None:
        self.json_a = json_a if json_a is not None else {}
        self.json_b = json_b if json_b is not None else {}
        self.diff_store: DffStoreType = {}
        self.diff_printer = diff_printer if diff_printer is not None else DiffPrinter()

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

    def _diff_node(
        self,
        json_a: JsonType | PrimitiveDataType,
        json_b: JsonType | PrimitiveDataType,
        tokenizer: Tokenizer,
    ):
        if self._is_mismatched(json_a, json_b):
            self.diff_store[tokenizer.token()] = DiffEnum.MISMATCHED
            return

        if isinstance(json_a, dict):
            longer_iterable: Dict[str, Any] = (
                json_b if len(json_a) < len(json_b) else json_a
            )
            for key in longer_iterable.keys():
                tokenizer.insert(key)
                if key not in json_a:
                    self.diff_store[tokenizer.token()] = DiffEnum.MISSING_LEFT
                    continue
                elif key not in json_b:
                    self.diff_store[tokenizer.token()] = DiffEnum.MISSING_RIGHT
                    continue
                self._diff_node(json_a[key], json_b[key], tokenizer)
                tokenizer.pop()
        elif isinstance(json_a, list):
            larger_len = len(json_b) if len(json_a) < len(json_b) else len(json_a)
            for idx in range(larger_len):
                tokenizer.insert(idx)
                if idx >= len(json_a):
                    self.diff_store[tokenizer.token()] = DiffEnum.MISSING_LEFT
                    continue
                elif idx >= len(json_b):
                    self.diff_store[tokenizer.token()] = DiffEnum.MISSING_RIGHT
                    continue
                self._diff_node(json_a[idx], json_b[idx], tokenizer)
                tokenizer.pop()

    def print(self):
        self.diff_printer.print(self.diff_store)