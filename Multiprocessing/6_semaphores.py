import time
import random
from multiprocessing import Process, Semaphore

def worker(sem, idx):
    print(f"Worker {idx} waiting for semaphore…")

    with sem:
        print(f"→ Worker {idx} ENTERED critical section ({sem})")
        # simulate some work
        time.sleep(random.uniform(1, 3))
        print(f"← Worker {idx} LEAVING critical section ({sem})")
    print(f"← Worker {idx} LEFT critical section ({sem})")

if __name__ == "__main__":
    # only 2 workers may hold the semaphore at once
    sem = Semaphore(2)

    procs = [Process(target=worker, args=(sem, i)) for i in range(6)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

