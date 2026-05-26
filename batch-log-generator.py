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

BASE_DAY = 1
BASE_HOUR = 9
BASE_MINUTE = 0
BASE_SECOND = 0

BATCH_INTERVAL_MINUTES = 15

MIN_ELAPSED_SEC = 2
MAX_ELAPSED_SEC = 8

BATCH_NAMES = [
    "daily_import",
    "user_sync",
    "order_export",
]

MIN_RECORD_COUNT = 100
MAX_RECORD_COUNT = 2000

STATUS_SUCCESS_RATE = 0.8

STATUS_START = "START"
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED = "FAILED"

ERROR_MESSAGES = [
    "connection timeout",
    "validation error",
    "file not found",
]


# =========================
# ログ生成処理
# =========================
def generate_batch_logs(seed=None):
    rng = random.Random(seed)
    logs = []

    now = datetime.now()
    base_time = datetime(now.year, now.month, BASE_DAY, BASE_HOUR, BASE_MINUTE, BASE_SECOND)
    days_in_month = calendar.monthrange(
        base_time.year,
        base_time.month
    )[1]

    for day in range(days_in_month):
        current_day = base_time + timedelta(days=day)

        for i, batch_name in enumerate(BATCH_NAMES):
            start_time = current_day + timedelta(minutes=i * BATCH_INTERVAL_MINUTES)
            end_time = start_time + timedelta(
                seconds=rng.randint(MIN_ELAPSED_SEC, MAX_ELAPSED_SEC)
            )

            success = rng.random() < STATUS_SUCCESS_RATE

            record_count = (
                rng.randint(MIN_RECORD_COUNT, MAX_RECORD_COUNT)
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
                "status": STATUS_START,
                "record_count": 0,
                "elapsed_sec": 0.00,
                "message": "job started",
            })

            logs.append({
                "timestamp": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "batch_name": batch_name,
                "status": STATUS_SUCCESS if success else STATUS_FAILED,
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