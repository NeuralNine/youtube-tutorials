use pyo3::prelude::*;

#[pymodule]
mod simple_extension {
    use pyo3::prelude::*;

    #[pyfunction]   
    fn greet_name(name: &str) -> PyResult<String> {
        Ok(format!("Hello, {}", name))
    }

    #[pyfunction]
    fn sum_list(numbers: Vec<i64>) -> PyResult<i64> {
        Ok(numbers.iter().sum())
    }

    #[pyfunction]
    fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
        Ok((a + b).to_string())
    }
}
