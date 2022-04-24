from src.json_differ import JsonDiffer


if __name__ == "__main__":
    differ = JsonDiffer({"1": 2}, {"1": 2})
    differ.generate_diffs()
