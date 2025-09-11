import time
import threading
import fast_factorial_repetition


def worker(n, n_repetitions):
    fast_factorial_repetition.factorial_without_GIL(n, n_repetitions)


if __name__ == '__main__':
    threads = [
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000)),
        # threading.Thread(target=worker, args=(20, 5_000_000))

        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000)),
        threading.Thread(target=worker, args=(20, 500_000_000))
    ]

    start = time.perf_counter()

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    end = time.perf_counter()

    print(end-start)

