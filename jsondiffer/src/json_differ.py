from typing import Dict, List, Union, Any


class JsonDiffer(object):
    def __init__(self, json_a: Union[Dict, List] = None, json_b: Union[Dict, List] = None) -> None:
        self.json_a = json_a
        self.json_b = json_b