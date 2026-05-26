from pathlib import Path
from datetime import datetime, timedelta
import random
import calendar
import csv


# =========================
# 設定値
# =========================
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR / "output" / "logs.csv"

SEED = 42

BATCH_NAMES = [
    "daily_import",
    "user_sync",
    "order_export",
]

STATUS_SUCCESS_RATE = 0.8

ERROR_MESSAGES = [
    "connection timeout",
    "validation error",
    "file not found",
]


# =========================
# ダミーログ生成処理
# =========================
def generate_batch_logs(seed=None):
    rng = random.Random(seed)
    logs = []

    now = datetime.now()
    base_time = datetime(now.year, now.month, 1, 9, 0, 0)
    days_in_month = calendar.monthrange(
        base_time.year,
        base_time.month
    )[1]

    for day in range(days_in_month):
        current_day = base_time + timedelta(days=day)

        for i, batch_name in enumerate(BATCH_NAMES):
            start_time = current_day + timedelta(minutes=i * 15)
            end_time = start_time + timedelta(
                seconds=rng.randint(2, 8)
            )

            success = rng.random() < STATUS_SUCCESS_RATE

            record_count = (
                rng.randint(100, 2000)
                if success else 0
            )

            message = (
                "job completed"
                if success
                else rng.choice(ERROR_MESSAGES)
            )

            logs.append({
                "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "batch_name": batch_name,
                "status": "START",
                "record_count": 0,
                "elapsed_sec": 0.00,
                "message": "job started",
            })

            logs.append({
                "timestamp": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "batch_name": batch_name,
                "status": "SUCCESS" if success else "FAILED",
                "record_count": record_count,
                "elapsed_sec": round(
                    (end_time - start_time).total_seconds(),
                    2
                ),
                "message": message,
            })

    return logs


# =========================
# CSV書き込み処理
# =========================
def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp",
                "batch_name",
                "status",
                "record_count",
                "elapsed_sec",
                "message"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)


# =========================
# main処理
# =========================
def main():
    logs = generate_batch_logs(SEED)
    write_csv(OUTPUT_PATH, logs)


if __name__ == "__main__":
    main()