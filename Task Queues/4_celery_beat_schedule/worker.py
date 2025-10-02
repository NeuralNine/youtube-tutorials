import os
from datetime import datetime

from celery import Celery
from celery.schedules import schedule, crontab

app = Celery(
    "ticker",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL"),
)

OUTPUT_PATH = "/data/timestamp.txt"

@app.task
def write_timestamp():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
        f.write(datetime.now().isoformat() + "\n")


app.conf.beat_schedule = {
    "timestamp_writer": {
        "task": "worker.write_timestamp",
        "schedule": schedule(10.0),  # every 10 seconds
    }
}

app.conf.beat_schedule = {
    "nightly-job": {
        "task": "worker.write_timestamp",
        "schedule": crontab(minute=21, hour=13),  # 03:15 every day
    }
}

app.conf.timezone = 'Europe/Vienna'
app.conf.enable_utc = True

