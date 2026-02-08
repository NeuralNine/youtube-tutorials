use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
mod perf_extension {
    use pyo3::prelude::*;

    #[pyfunction]
    fn find_primes(n: usize) -> Vec<usize> {
        let mut is_prime = vec![true; n + 1];
        is_prime[0] = false;
        is_prime[1] = false;

        let mut p = 2;
        while p * p <= n {
            if is_prime[p] {
                for multiple in (p * p..=n).step_by(p) {
                    is_prime[multiple] = false;
                }
            }
            p += 1;
        }

        is_prime.iter().enumerate()
            .filter(|&(_, &prime)| prime)
            .map(|(i, _)| i)
            .collect()
    }

}
