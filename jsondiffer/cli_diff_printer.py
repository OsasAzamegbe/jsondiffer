from jsondiffer.custom_types import DffStoreType, JsonType, PrimitiveDataType
from jsondiffer.diff_printer import DiffPrinter
from jsondiffer.tokenizer import Tokenizer

ADDITION_PREFIX = "+"
SUBTRACTION_PREFIX = "-"
INDENTATION = "    "
INDENTATION_SIZE = len(INDENTATION)


class CliDiffPrinter(DiffPrinter):
    @staticmethod
    def _print_to_cli(
        padding: str, *args, prefix: str = "", new_line: bool = False, **kwargs
    ):
        if new_line:
            prefix = "\n" + prefix
        print(prefix + padding, *args, end="", **kwargs)

    def _print_json_node_to_cli(
        self,
        json_a: JsonType | PrimitiveDataType,
        json_b: JsonType | PrimitiveDataType,
        tokenizer: Tokenizer,
        padding: str = "",
    ):
        if isinstance(json_a, PrimitiveDataType):
            if isinstance(json_a, str):
                json_a = f'"{json_a}"'
            elif isinstance(json_a, bool):
                json_a = "true" if json_a else "false"
            elif json_a is None:
                json_a = "null"
            self._print_to_cli("", json_a)
        elif isinstance(json_a, dict):
            self._print_to_cli("", "{")
            padding += INDENTATION
            not_last_key = len(json_a)
            for key, value in json_a.items():
                tokenizer.insert(key)
                not_last_key -= 1
                self._print_to_cli(padding, f'"{key}":', new_line=True)
                self._print_json_node_to_cli(value, json_b.get(key), tokenizer, padding)
                if not_last_key:
                    self._print_to_cli(",")
                tokenizer.pop()
            padding = padding[:-INDENTATION_SIZE]
            self._print_to_cli(padding, "}", new_line=True)
        elif isinstance(json_a, list):
            self._print_to_cli("", "[")
            padding += INDENTATION
            not_last_key = len(json_a)
            for idx, value in enumerate(json_a):
                tokenizer.insert(idx)
                not_last_key -= 1
                self._print_to_cli(padding, new_line=True)
                self._print_json_node_to_cli(value, json_b[idx], tokenizer, padding)
                if not_last_key:
                    self._print_to_cli(",")
                tokenizer.pop()
            padding = padding[:-INDENTATION_SIZE]
            self._print_to_cli(padding, "]", new_line=True)

    def print(self, diff_store: DffStoreType):
        self.diff_store = diff_store
        self._print_json_node_to_cli(self.json_a, self.json_b, Tokenizer())
