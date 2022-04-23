from typing import Any
import pytest
from typing import Any
from jsondiffer.src.json_differ import JsonDiffer


valid_json_string = """{"int": 1, "bool": false, "status": "This JSON is valid"}"""
invalid_json_string = """{"int": 1, "bool": false "status": "This JSON is NOT valid"}"""


@pytest.mark.parametrize(
    "json_data,expected_result",
    [(valid_json_string, True), (invalid_json_string, False)],
    ids=["JSON_from_string_is_valid", "JSON_from_string_is_not_valid"],
)
def test_json_validator(json_data: Any, expected_result: bool):
    assert JsonDiffer.is_valid_json(json_data) == expected_result
