from typing import Any, Tuple
from unittest.mock import Mock
import pytest
import os
from jsondiffer.custom_types import JsonType, TokenType

from jsondiffer.diff_enum import DiffEnum
from jsondiffer.json_differ import JsonDiffer

# test static methods
valid_json_string = """{"int": 1, "bool": false, "status": "This JSON is valid"}"""
invalid_json_string = """{"int": 1, "bool": false "status": "This JSON is NOT valid"}"""
valid_json_path = os.path.join(os.path.dirname(__file__), "valid_json.json")
invalid_json_path = os.path.join(os.path.dirname(__file__), "invalid_json.json")


@pytest.mark.parametrize(
    "json_data,expected_result,is_file",
    [
        (valid_json_string, True, False),
        (invalid_json_string, False, False),
        (valid_json_path, True, True),
        (invalid_json_path, False, True),
    ],
    ids=[
        "JSON_from_string_is_valid",
        "JSON_from_string_is_not_valid",
        "JSON_from_file_is_valid",
        "JSON_from_file_is_not_valid",
    ],
)
def test_json_validator(json_data: Any, expected_result: bool, is_file: bool):
    assert JsonDiffer.is_valid_json(json_data, is_file) == expected_result


def test_is_json_loadable_returns_true():
    mock_func = Mock()
    json_string = "[test]"
    assert JsonDiffer._is_json_loadable(mock_func, json_string)
    mock_func.assert_called_once_with(json_string)


def test_is_json_loadable_returns_false():
    mock_func = Mock()
    mock_func.side_effect = ValueError()
    json_string = "[test]"
    assert not JsonDiffer._is_json_loadable(mock_func, json_string)
    mock_func.assert_called_once_with(json_string)


@pytest.mark.parametrize(
    "json_a,json_b,expected",
    [
        ({"type": "dict"}, ["list"], True),
        (["list", "test"], ["list"], False),
        (["list"], ["list"], False),
        ("str", None, True),
        (None, None, False),
        ("str", "str1", True),
        ("str", "str", False),
        (1, 2, True),
        (1, 1, False),
        (1.000, 1.012, True),
        (1.012, 1.012, False),
        (True, False, True),
        (True, True, False),
    ],
)
def test_is_mismatched(json_a, json_b, expected: bool):
    assert JsonDiffer._is_mismatched(json_a, json_b) == expected


@pytest.mark.parametrize(
    "json_a,json_b,expected_diff_keys,expected_diffs",
    [
        ({"first": 1}, {"first": 1}, (None,), (None,)),
        (
            {"first": [1, {"second": "test"}]},
            {"first": [1, {"second": "test"}]},
            (None,),
            (None,),
        ),
        (
            {"first": 1, "second": {"third": False}},
            {"first": 1, "second": {"third": False}},
            (None,),
            (None,),
        ),
        ({"first": 1}, {"first": 2}, (("first",),), (DiffEnum.MISMATCHED,)),
        (
            {"first": [1, {"second": "test"}]},
            {"first": [1, {"second": "not test"}]},
            (("first", 1, "second"),),
            (DiffEnum.MISMATCHED,),
        ),
        (
            {"first": [1, {"second": []}]},
            {"first": [1, {"second": {}}]},
            (("first", 1, "second"),),
            (DiffEnum.MISMATCHED,),
        ),
        (
            {"first": 1, "second": {"third": False}},
            {"first": 1, "second": {"third": True}},
            (
                (
                    "second",
                    "third",
                ),
            ),
            (DiffEnum.MISMATCHED,),
        ),
        ({"first": 1}, {}, (("first",),), (DiffEnum.MISSING_RIGHT,)),
        ({}, {"first": 1}, (("first",),), (DiffEnum.MISSING_LEFT,)),
        (
            {"first": 1, "second": ["a", "b", "c", [1, 2, 3, 4]]},
            {"first": 1, "second": ["a", "b", "c"]},
            (("second", 3),),
            (DiffEnum.MISSING_RIGHT,),
        ),
        (
            {"first": 1, "second": ["a", "b", "c"]},
            {"first": 1, "second": ["a", "b", "c", [1, 2, 3, 4]]},
            (("second", 3),),
            (DiffEnum.MISSING_LEFT,),
        ),
    ],
)
def test_generate_diffs(
    json_a: JsonType,
    json_b: JsonType,
    expected_diff_keys: Tuple[TokenType],
    expected_diffs: Tuple[DiffEnum],
):
    differ = JsonDiffer(json_a, json_b)
    differ.generate_diffs()

    for expected_diff, expected_diff_key in zip(expected_diffs, expected_diff_keys):
        if expected_diff_key:
            assert expected_diff_key in differ.diff_store
            assert expected_diff == differ.diff_store.get(expected_diff_key)
        else:
            assert len(differ.diff_store) == 0
