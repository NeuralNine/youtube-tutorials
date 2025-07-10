import time
import math
from multiprocessing import Pool

if __name__ == '__main__':
    start = time.perf_counter()
    results1 = [math.factorial(x) for x in range(12000)]
    end = time.perf_counter()

    print(end-start)

    start =  time.perf_counter()
    with Pool(5) as p:
        results2 = p.map(math.factorial, list(range(12000)))
    end =  time.perf_counter()

    print(end - start)

    print(all(x == y for x, y in zip(results1, results2)))
