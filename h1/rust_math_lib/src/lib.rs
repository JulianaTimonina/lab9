use pyo3::prelude::*;
use pyo3::types::PyModule;

/// Сумма квадратов чисел
#[pyfunction]
fn sum_squares(numbers: Vec<i64>) -> i64 {
    numbers.iter().map(|x| x * x).sum()
}

/// Быстрое вычисление факториала
#[pyfunction]
fn factorial(n: u64) -> u64 {
    (1..=n).product()
}

/// Быстрая сортировка
#[pyfunction]
fn quick_sort(mut numbers: Vec<i64>) -> Vec<i64> {
    numbers.sort_unstable();
    numbers
}

/// Числа Фибоначчи
#[pyfunction]
fn fibonacci(n: u32) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => {
            let mut a = 0u64;
            let mut b = 1u64;
            for _ in 2..=n {
                let c = a + b;
                a = b;
                b = c;
            }
            b
        }
    }
}

/// Класс для математических операций
#[pyclass]
struct MathOperations {
    #[pyo3(get, set)]
    value: f64,
}

#[pymethods]
impl MathOperations {
    #[new]
    fn new(value: f64) -> Self {
        MathOperations { value }
    }
    
    fn square(&self) -> f64 {
        self.value * self.value
    }
    
    fn cube(&self) -> f64 {
        self.value * self.value * self.value
    }
}

/// Модуль Python
#[pymodule]
fn lab9_rust_math_lib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_squares, m)?)?;
    m.add_function(wrap_pyfunction!(factorial, m)?)?;
    m.add_function(wrap_pyfunction!(quick_sort, m)?)?;
    m.add_function(wrap_pyfunction!(fibonacci, m)?)?;
    m.add_class::<MathOperations>()?;
    Ok(())
}