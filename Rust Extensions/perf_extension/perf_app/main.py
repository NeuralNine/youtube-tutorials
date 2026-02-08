import time
import perf_extension

def py_find_primes(n: int) -> list[int]:
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= n:
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1

    return [i for i, prime in enumerate(is_prime) if prime]


n = 100_000_000

start = time.perf_counter()
py_result = py_find_primes(n)
end = time.perf_counter()
py_time = end - start

start = time.perf_counter()
rust_result = perf_extension.find_primes(n)
end = time.perf_counter()
rust_time = end - start

print(f'Python Time: {py_time}')
print(f'Rust Time: {rust_time}')
print(f'Speedup: {py_time/rust_time}x Faster')

