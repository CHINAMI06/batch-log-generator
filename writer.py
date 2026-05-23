import csv
from pathlib import Path


def write_csv(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "batch_name", "status",
            "record_count", "elapsed_sec", "message"
        ])
        writer.writeheader()
        writer.writerows(rows)