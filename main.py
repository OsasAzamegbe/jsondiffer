import argparse
import json
from jsondiffer.cli_diff_printer import CliDiffPrinter

from jsondiffer.json_differ import JsonDiffer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("JSON_FILE_1", type=argparse.FileType("rb"), help="First JSON file")
    parser.add_argument("JSON_FILE_2", type=argparse.FileType("rb"), help="Second JSON file")
    args = parser.parse_args()
    json_bytes_a = args.JSON_FILE_1.read()
    json_bytes_b = args.JSON_FILE_2.read()

    if not JsonDiffer.is_valid_json(json_bytes_a) or not JsonDiffer.is_valid_json(
        json_bytes_b
    ):
        parser.error("arguments passed must be valid json file paths")

    json_a = json.loads(json_bytes_a)
    json_b = json.loads(json_bytes_b)

    differ = JsonDiffer(json_a, json_b, CliDiffPrinter(json_a, json_b))
    differ.generate_diffs()
    differ.print()

    args.JSON_FILE_1.close()
    args.JSON_FILE_2.close()
