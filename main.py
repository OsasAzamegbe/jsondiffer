import argparse
import json

from jsondiffer.json_differ import JsonDiffer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file_1", type=argparse.FileType("rb"))
    parser.add_argument("json_file_2", type=argparse.FileType("rb"))
    args = parser.parse_args()
    json_bytes_a = args.json_file_1.read()
    json_bytes_b = args.json_file_2.read()

    if not JsonDiffer.is_valid_json(json_bytes_a) or not JsonDiffer.is_valid_json(
        json_bytes_b
    ):
        parser.error("arguments passed must be valid json file paths")

    json_a = json.loads(json_bytes_a)
    json_b = json.loads(json_bytes_b)

    differ = JsonDiffer(json_a, json_b)
    differ.generate_diffs()

    args.json_file_1.close()
    args.json_file_2.close()
