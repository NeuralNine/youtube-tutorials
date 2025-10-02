import time

from celery.result import AsyncResult

from worker import movie_info, app

time.sleep(5)

result_future1 = movie_info.delay('Tell me about the movie Shutter Island.')
result_future2 = movie_info.delay('Tell me about the movie Inception.')
result_future3 = movie_info.delay('Tell me about the movie Predestination.')

result_futures = [result_future1, result_future2, result_future3]
results = [AsyncResult(rf.id, app=app) for rf in result_futures]

print("We can immediately proceed with the remaining programming logic and don't need to wait for completion")

while True:
    if not results:
        break

    for r in results:
        # if r.state == 'SUCCESS':
        if r.ready():
            print(r.get())
            results.remove(r)

    time.sleep(1)

