from pathlib import Path
from datetime import datetime, timedelta
import random
import calendar
import csv


# =========================
# 設定値
# =========================
NOW = datetime.now()
NOW_TODAY = NOW.strftime("%Y%m%d")
NOW_TIME = NOW.strftime('%Y%m%d%H%M')

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR / "output" /  NOW_TODAY /f"logs_ver{NOW_TIME}.csv"

BASE_DAY = 1
BASE_HOUR = 9
BASE_MINUTE = 0
BASE_SECOND = 0

# テスト用の固定値設定（結果を変化させたい場合はNoneが必要です）
#TEST_BASE_TIME = datetime(2026, 4, BASE_DAY, BASE_HOUR, BASE_MINUTE, BASE_SECOND) 
TEST_BASE_TIME = None
#SEED = 42
SEED = None

BATCH_INTERVAL_MINUTES = 15

ELAPSED_SEC_ZERO = 0.00
MIN_ELAPSED_SEC = 2
MAX_ELAPSED_SEC = 8

BATCH_NAMES = [
    "daily_import.bat",
    "user_sync.bat",
    "order_export.bat",
]

RECORD_COUNT_ZERO = 0
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
def create_log(
    timestamp,
    batch_name,
    status,
    record_count,
    elapsed_sec,
    message,
    ):
    return {
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "batch_name": batch_name,
        "status": status,
        "record_count": record_count,
        "elapsed_sec": elapsed_sec,
        "message": message,
    }

def generate_batch_logs(seed=None, base_time=None):
    rng = random.Random(seed)
    logs = []

    if base_time is None:
        base_time = datetime(NOW.year, NOW.month, BASE_DAY, BASE_HOUR, BASE_MINUTE, BASE_SECOND)
    
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
                if success else RECORD_COUNT_ZERO
            )

            message = (
                "job completed"
                if success
                else rng.choice(ERROR_MESSAGES)
            )

            logs.append(
                create_log(
                    start_time,
                    batch_name,
                    STATUS_START,
                    RECORD_COUNT_ZERO,
                    ELAPSED_SEC_ZERO,
                    "job started",
                )
            )

            logs.append(
                create_log(
                    end_time,
                    batch_name,
                    STATUS_SUCCESS if success else STATUS_FAILED,
                    record_count,
                    round(
                        (end_time - start_time).total_seconds(),
                        2
                    ),
                    message,
                )
            )

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
    try:
        logs = generate_batch_logs(SEED, TEST_BASE_TIME)
        write_csv(OUTPUT_PATH, logs)

    except Exception as e:
        print(f"error occurred: {e}")
    
    else:
        print(f"Logs generated: {OUTPUT_PATH}")

    finally:
        print("Process completed.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()