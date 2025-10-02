import os
import time
import random

from celery import Celery

app = Celery(
    'random_number',
    broker = os.getenv('CELERY_BROKER_URL'),
    backend = os.getenv('CELERY_BACKEND_URL')
)


@app.task
def random_number(max_value):
    time.sleep(5)
    return random.randint(0, 100)

