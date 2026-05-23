from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR / "output" / "logs.csv"

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

