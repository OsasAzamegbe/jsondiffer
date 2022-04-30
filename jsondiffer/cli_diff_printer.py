from pyparsing import col
from jsondiffer.custom_types import DiffStoreType, JsonType, PrimitiveDataType
from jsondiffer.diff_enum import DiffEnum
from jsondiffer.diff_printer import DiffPrinter
from jsondiffer.tokenizer import Tokenizer

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

    def _print_dict_key_value_to_cli(
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
        self._print_json_node_to_cli(value, json_b, tokenizer, padding, color=color)
        if not_last_key:
            self._print_to_cli(",", color=color)

    def _print_json_node_to_cli(
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
            self._print_to_cli("", "{", color=color)
            padding += INDENTATION
            not_last_key = len(json_a)
            for key, value in json_a.items():
                tokenizer.insert(key)
                not_last_key -= 1
                token = tokenizer.token()
                if token in self.diff_store:
                    if self.diff_store[token] == DiffEnum.MISMATCHED:
                        self._print_dict_key_value_to_cli(
                            key,
                            value,
                            value,
                            tokenizer,
                            ADDITION_PREFIX + padding[:-1],
                            not_last_key,
                            color=OK_COLOR,
                        )
                        self._print_dict_key_value_to_cli(
                            key,
                            json_b[key],
                            json_b[key],
                            tokenizer,
                            SUBTRACTION_PREFIX + padding[:-1],
                            not_last_key,
                            color=FAIL_COLOR,
                        )
                    elif self.diff_store[token] == DiffEnum.MISSING_LEFT:
                        self._print_dict_key_value_to_cli(
                            key,
                            json_b[key],
                            json_b[key],
                            tokenizer,
                            SUBTRACTION_PREFIX + padding[:-1],
                            not_last_key,
                            color=FAIL_COLOR,
                        )
                    if self.diff_store[token] == DiffEnum.MISSING_RIGHT:
                        self._print_dict_key_value_to_cli(
                            key,
                            value,
                            value,
                            tokenizer,
                            ADDITION_PREFIX + padding[:-1],
                            not_last_key,
                            color=OK_COLOR,
                        )
                else:
                    self._print_dict_key_value_to_cli(
                        key,
                        value,
                        json_b[key],
                        tokenizer,
                        padding,
                        not_last_key,
                        color=color,
                    )
                tokenizer.pop()
            padding = padding[:-INDENTATION_SIZE]
            self._print_to_cli(padding, "}", new_line=True, color=color)
        elif isinstance(json_a, list):
            self._print_to_cli("", "[", color=color)
            padding += INDENTATION
            not_last_key = len(json_a)
            for idx, value in enumerate(json_a):
                tokenizer.insert(idx)
                not_last_key -= 1
                self._print_to_cli(padding, new_line=True, color=color)
                self._print_json_node_to_cli(
                    value, json_b[idx], tokenizer, padding, color=color
                )
                if not_last_key:
                    self._print_to_cli(",", color=color)
                tokenizer.pop()
            padding = padding[:-INDENTATION_SIZE]
            self._print_to_cli(padding, "]", new_line=True, color=color)

    def print(self, diff_store: DiffStoreType):
        self.diff_store = diff_store
        self._print_json_node_to_cli(self.json_a, self.json_b, Tokenizer())
