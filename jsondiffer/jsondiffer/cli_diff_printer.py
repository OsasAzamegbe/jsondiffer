from typing import Dict, List

from jsondiffer.jsondiffer.custom_types import (
    DiffStoreType,
    JsonType,
    PrimitiveDataType,
)
from jsondiffer.jsondiffer.diff_enum import DiffEnum
from jsondiffer.jsondiffer.diff_printer import DiffPrinter
from jsondiffer.jsondiffer.tokenizer import Tokenizer

ADDITION_PREFIX = "+"
SUBTRACTION_PREFIX = "-"
INDENTATION = "    "
INDENTATION_SIZE = len(INDENTATION)
OK_COLOR = "\033[92m"
FAIL_COLOR = "\033[91m"
NORMAL_COLOR = "\033[0m"


class CliDiffPrinter(DiffPrinter):
    @staticmethod
    def _print_to_cli(
        padding: str,
        *args,
        prefix: str = "",
        new_line: bool = False,
        color: str = NORMAL_COLOR,
        **kwargs,
    ):
        if new_line:
            prefix = "\n" + prefix
        print(color + prefix + padding, *args, end="", **kwargs)

    def _output_dict_key_value_pair_to_stdout(
        self,
        key: str,
        value: JsonType | PrimitiveDataType,
        json_b: JsonType | PrimitiveDataType,
        tokenizer: Tokenizer,
        padding: str,
        not_last_key: int,
        color: str = NORMAL_COLOR,
    ):
        self._print_to_cli(padding, f'"{key}":', new_line=True, color=color)
        self._output_json_and_diffs_to_stdout(
            value, json_b, tokenizer, padding, color=color
        )
        if not_last_key:
            self._print_to_cli(",", color=color)

    def _output_list_value_to_stdout(
        self,
        json_a_value: JsonType | PrimitiveDataType,
        json_b_value: JsonType | PrimitiveDataType,
        tokenizer: Tokenizer,
        padding: str,
        not_last_key: int,
        color: str = NORMAL_COLOR,
    ):
        self._print_to_cli(padding, new_line=True, color=color)
        self._output_json_and_diffs_to_stdout(
            json_a_value,
            json_b_value,
            tokenizer,
            padding,
            color=color,
        )
        if not_last_key:
            self._print_to_cli(",", color=color)

    def _output_dict_and_diffs_to_stdout(
        self,
        json_a: Dict,
        json_b: Dict,
        tokenizer: Tokenizer,
        padding: str,
        color: str,
    ):
        self._print_to_cli("", "{", color=color)
        padding += INDENTATION

        keys_set: List[str] = list(json_a.keys())
        keys_set.extend(key for key in json_b.keys() if key not in json_a)
        not_last_key = len(keys_set)
        for key in keys_set:
            tokenizer.insert(key)
            not_last_key -= 1
            token = tokenizer.token()
            if token in self.diff_store:
                self._print_to_cli("", new_line=True)
                if self.diff_store[token] == DiffEnum.MISMATCHED:
                    self._output_dict_key_value_pair_to_stdout(
                        key,
                        json_a[key],
                        json_a[key],
                        tokenizer,
                        ADDITION_PREFIX + padding[:-1],
                        not_last_key,
                        color=OK_COLOR,
                    )
                    self._output_dict_key_value_pair_to_stdout(
                        key,
                        json_b[key],
                        json_b[key],
                        tokenizer,
                        SUBTRACTION_PREFIX + padding[:-1],
                        not_last_key,
                        color=FAIL_COLOR,
                    )
                elif self.diff_store[token] == DiffEnum.MISSING_LEFT:
                    self._output_dict_key_value_pair_to_stdout(
                        key,
                        json_b[key],
                        json_b[key],
                        tokenizer,
                        SUBTRACTION_PREFIX + padding[:-1],
                        not_last_key,
                        color=FAIL_COLOR,
                    )
                elif self.diff_store[token] == DiffEnum.MISSING_RIGHT:
                    self._output_dict_key_value_pair_to_stdout(
                        key,
                        json_a[key],
                        json_a[key],
                        tokenizer,
                        ADDITION_PREFIX + padding[:-1],
                        not_last_key,
                        color=OK_COLOR,
                    )
                self._print_to_cli("", new_line=True)
            else:
                self._output_dict_key_value_pair_to_stdout(
                    key,
                    json_a[key],
                    json_b[key],
                    tokenizer,
                    padding,
                    not_last_key,
                    color=color,
                )
            tokenizer.pop()
        padding = padding[:-INDENTATION_SIZE]
        self._print_to_cli(padding, "}", new_line=True, color=color)

    def _output_list_and_diffs_to_stdout(
        self,
        json_a: List,
        json_b: List,
        tokenizer: Tokenizer,
        padding: str,
        color: str,
    ):
        self._print_to_cli("", "[", color=color)
        padding += INDENTATION

        larger_len = len(json_b) if len(json_a) < len(json_b) else len(json_a)
        not_last_key = larger_len
        for idx in range(larger_len):
            tokenizer.insert(idx)
            not_last_key -= 1
            json_a_value = json_a[idx] if idx < len(json_a) else json_b[idx]
            json_b_value = json_b[idx] if idx < len(json_b) else json_a[idx]

            token = tokenizer.token()
            if token in self.diff_store:
                self._print_to_cli("", new_line=True)
                if self.diff_store[token] == DiffEnum.MISMATCHED:
                    self._output_list_value_to_stdout(
                        json_a_value,
                        json_a_value,
                        tokenizer,
                        ADDITION_PREFIX + padding[:-1],
                        not_last_key,
                        color=OK_COLOR,
                    )
                    self._output_list_value_to_stdout(
                        json_b_value,
                        json_b_value,
                        tokenizer,
                        SUBTRACTION_PREFIX + padding[:-1],
                        not_last_key,
                        color=FAIL_COLOR,
                    )
                elif self.diff_store[token] == DiffEnum.MISSING_LEFT:
                    self._output_list_value_to_stdout(
                        json_b_value,
                        json_b_value,
                        tokenizer,
                        SUBTRACTION_PREFIX + padding[:-1],
                        not_last_key,
                        color=FAIL_COLOR,
                    )
                elif self.diff_store[token] == DiffEnum.MISSING_RIGHT:
                    self._output_list_value_to_stdout(
                        json_a_value,
                        json_a_value,
                        tokenizer,
                        ADDITION_PREFIX + padding[:-1],
                        not_last_key,
                        color=OK_COLOR,
                    )
                self._print_to_cli("", new_line=True)
            else:
                self._output_list_value_to_stdout(
                    json_a_value,
                    json_b_value,
                    tokenizer,
                    padding,
                    not_last_key,
                    color=color,
                )
            tokenizer.pop()
        padding = padding[:-INDENTATION_SIZE]
        self._print_to_cli(padding, "]", new_line=True, color=color)

    def _output_json_and_diffs_to_stdout(
        self,
        json_a: JsonType | PrimitiveDataType,
        json_b: JsonType | PrimitiveDataType,
        tokenizer: Tokenizer,
        padding: str = "",
        color: str = NORMAL_COLOR,
    ):
        if isinstance(json_a, PrimitiveDataType):
            if isinstance(json_a, str):
                json_a = f'"{json_a}"'
            elif isinstance(json_a, bool):
                json_a = "true" if json_a else "false"
            elif json_a is None:
                json_a = "null"
            self._print_to_cli("", json_a, color=color)
        elif isinstance(json_a, dict):
            self._output_dict_and_diffs_to_stdout(
                json_a, json_b, tokenizer, padding, color
            )
        elif isinstance(json_a, list):
            self._output_list_and_diffs_to_stdout(
                json_a, json_b, tokenizer, padding, color
            )

    def print(self, diff_store: DiffStoreType):
        self.diff_store = diff_store
        self._output_json_and_diffs_to_stdout(self.json_a, self.json_b, Tokenizer())
