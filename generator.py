from datetime import datetime, timedelta
import random, calendar
from config import BATCH_NAMES, STATUS_SUCCESS_RATE, ERROR_MESSAGES


def generate_batch_logs(seed=None):
    rng = random.Random(seed)
    logs = []

    now = datetime.now()
    base_time = datetime(now.year, now.month, 1, 9, 0, 0)
    days_in_month = calendar.monthrange(base_time.year, base_time.month)[1]

    for day in range(days_in_month):
        days=base_time + timedelta(days=day)

        for i, batch_name in enumerate(BATCH_NAMES):
            start_time = days + timedelta(minutes=i * 15)
            end_time = start_time + timedelta(seconds=rng.randint(2, 8))
            success = rng.random() < STATUS_SUCCESS_RATE
            record_count = rng.randint(100, 2000) if success else 0
            message = "job completed" if success else rng.choice(ERROR_MESSAGES)

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

