import time
import threading


def factorial(n):
    r = 1

    for i in range(1, n+1):
        r *= i

    return r


def worker(n, n_repetitions):
    for _ in range(n_repetitions):
        factorial(n)


if __name__ == '__main__':
    threads = [
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
        threading.Thread(target=worker, args=(20, 5_000_000)),
    ]

    start = time.perf_counter()

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    end = time.perf_counter()

    print(end-start)

