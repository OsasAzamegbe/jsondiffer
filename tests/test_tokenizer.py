from typing import List
import pytest

from jsondiffer.custom_types import DiffKeyType, TokenType
from jsondiffer.tokenizer import Tokenizer


@pytest.mark.parametrize(
    "key_list,expected_token",
    [
        (
            ["test", "a", "b", "c", 1, 2, 3],
            (
                "test",
                "a",
                "b",
                "c",
                1,
                2,
                3,
            ),
        ),
        ([], ()),
        ([1], (1,)),
    ],
)
def test_tokenizer_token(key_list: List[DiffKeyType], expected_token: TokenType):
    tokenizer = Tokenizer(key_list)
    assert expected_token == tokenizer.token()
