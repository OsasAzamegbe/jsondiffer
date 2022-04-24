from jsondiffer.diff_enum import DiffEnum
from jsondiffer.custom_types import DiffKeyType

from dataclasses import dataclass


@dataclass
class Diff(object):
    diff_type: DiffEnum
    key: DiffKeyType
