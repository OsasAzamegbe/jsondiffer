from src.json_differ import JsonDiffer


if __name__ == "__main__":
    differ = JsonDiffer(
        {"first": {"list": [1, 2, 3, 4], "int": 2}},
        {"first": {"list": [1, 2, 3], "int": 3}, "second": True},
    )
    differ.generate_diffs()
