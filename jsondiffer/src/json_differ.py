from typing import Callable, Union
from custom_types import JsonType
import json

class JsonDiffer(object):
    def __init__(
        self, json_a: JsonType = None, json_b: JsonType = None
    ) -> None:
        self.json_a = json_a if json_a is not None else {}
        self.json_b = json_b if json_b is not None else {}
        
    @staticmethod
    def is_json_loadable(load_function: Callable, json_data: Union[str, JsonType], *args, **kwargs) -> bool:
        try:
            load_function(json_data, *args, **kwargs)
        except ValueError as error:
            return False
        return True

    @staticmethod
    def is_valid_json(json_data: Union[str, JsonType], is_file: bool = False) -> bool:
        if is_file:
            return JsonDiffer.is_json_loadable(json.load, json_data)
        return JsonDiffer.is_json_loadable(json.loads, json_data)

