from multiprocessing import Process, Lock, Value

def worker(lock, counter):
    for _ in range(100000):
        with lock:  # try without lock
            counter.value += 1

if __name__ == "__main__":
    lock = Lock()
    counter = Value('i', 0)   # shared, synchronized integer

    procs = [Process(target=worker, args=(lock, counter)) for _ in range(4)]

    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print(counter.value)

