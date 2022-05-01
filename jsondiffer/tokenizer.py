from dataclasses import dataclass, field
from typing import List

from jsondiffer.custom_types import DiffKeyType, TokenType


@dataclass
class Tokenizer(object):
    token_list: List[DiffKeyType] = field(default_factory=list)

    def token(self) -> TokenType:
        return tuple(self.token_list)

    def insert(self, node: DiffKeyType):
        self.token_list.append(node)

    def pop(self):
        self.token_list.pop()
