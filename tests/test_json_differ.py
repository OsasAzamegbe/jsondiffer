from typing import Any
import pytest
from typing import Any
from jsondiffer.src.json_differ import JsonDiffer
import os


valid_json_string = """{"int": 1, "bool": false, "status": "This JSON is valid"}"""
invalid_json_string = """{"int": 1, "bool": false "status": "This JSON is NOT valid"}"""
valid_json_path = os.path.abspath("valid_json.json")
invalid_json_path = os.path.abspath("invalid_json.json")


@pytest.mark.parametrize(
    "json_data,expected_result,is_file",
    [
        (valid_json_string, True, False),
        (invalid_json_string, False, False),
        (valid_json_path, True, True),
        (invalid_json_path, False, True),
    ],
    ids=["JSON_from_string_is_valid", "JSON_from_string_is_not_valid", "JSON_from_file_is_valid", "JSON_from_file_is_not_valid"],
)
def test_json_validator(json_data: Any, expected_result: bool, is_file: bool):
    assert JsonDiffer.is_valid_json(json_data, is_file) == expected_result
