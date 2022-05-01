from abc import abstractmethod
from dataclasses import dataclass

from jsondiffer.jsondiffer.custom_types import JsonType


@dataclass
class DiffPrinter(object):
    json_a: JsonType
    json_b: JsonType

    @abstractmethod
    def print(self, *args):
        raise NotImplementedError
