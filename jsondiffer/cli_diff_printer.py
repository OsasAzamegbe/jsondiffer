from jsondiffer.custom_types import DffStoreType, JsonType, PrimitiveDataType
from jsondiffer.diff_printer import DiffPrinter
from jsondiffer.tokenizer import Tokenizer

ADDITION_PREFIX = "+"
SUBTRACTION_PREFIX = "-"


class CliDiffPrinter(DiffPrinter):
    @staticmethod
    def _print_to_cli(padding: str, *args, prefix: str = " ", **kwargs):
        print(prefix, padding, *args, **kwargs)

    def _print_json_node_to_cli(
        self,
        json_a: JsonType,
        json_b: JsonType,
        tokenizer: Tokenizer,
        padding: str = "",
        print_opening_bracket: bool = False,
    ):
        if isinstance(json_a, dict):
            if print_opening_bracket:
                self._print_to_cli(padding, "{")
            padding += "\t"
            for key, value in json_a.items():
                tokenizer.insert(key)

                if isinstance(value, PrimitiveDataType):
                    if isinstance(value, str):
                        value = f'"{value}"'
                    elif isinstance(value, bool):
                        value = "true" if value else "false"
                    elif value is None:
                        value = "null"
                    self._print_to_cli(padding, f'"{key}": {value},')
                else:
                    bracket = "{" if isinstance(value, dict) else "["
                    self._print_to_cli(padding, f'"{key}":', bracket)
                    self._print_json_node_to_cli(
                        value, json_b.get(key), tokenizer, padding
                    )
                tokenizer.pop()
            padding = padding[:-1]
            self._print_to_cli(padding, "}")

        elif isinstance(json_a, list):
            if print_opening_bracket:
                self._print_to_cli(padding, "[")
            padding += "\t"
            for idx, value in enumerate(json_a):
                tokenizer.insert(idx)
                if isinstance(value, PrimitiveDataType):
                    self._print_to_cli(padding, f"{value},")
                else:
                    bracket = "{" if isinstance(value, dict) else "["
                    self._print_to_cli(padding, bracket)
                    self._print_json_node_to_cli(value, json_b[idx], tokenizer, padding)
                tokenizer.pop()
            padding[:-1]
            self._print_to_cli(padding, "]")

    def print(self, diff_store: DffStoreType):
        self.diff_store = diff_store
        self._print_json_node_to_cli(
            self.json_a, self.json_b, Tokenizer(), print_opening_bracket=True
        )
