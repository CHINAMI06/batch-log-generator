from datetime import datetime, timedelta
import random
from config import BATCH_NAMES, STATUS_SUCCESS_RATE, ERROR_MESSAGES


def generate_batch_logs():
    logs = []
    base_time = datetime(2026, 5, 22, 9, 0, 0)

    for i, batch_name in enumerate(BATCH_NAMES):
        start_time = base_time + timedelta(minutes=i * 15)
        end_time = start_time + timedelta(seconds=random.randint(2, 8))
        success = random.random() < STATUS_SUCCESS_RATE
        record_count = random.randint(100, 2000) if success else 0
        message = "job completed" if success else random.choice(ERROR_MESSAGES)

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
            "elapsed_sec": round((end_time - start_time).total_seconds(), 2),
            "message": message,
        })

    return logs

