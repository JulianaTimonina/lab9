use pyo3::prelude::*;
use pyo3::types::PyDict;

/// Вычисление суммы квадратов чисел
#[pyfunction]
fn sum_squares(numbers: Vec<i64>) -> i64 {
    numbers.iter().map(|x| x * x).sum()
}

/// Обработка списка чисел с различными операциями
#[pyfunction]
fn process_numbers(py: Python, numbers: Vec<i64>) -> PyResult<PyObject> {
    let dict = PyDict::new(py);
    
    if numbers.is_empty() {
        dict.set_item("sum_squares", 0)?;
        dict.set_item("sum", 0)?;
        dict.set_item("max", py.None())?;
        dict.set_item("min", py.None())?;
        dict.set_item("average", 0.0)?;
        return Ok(dict.into());
    }
    
    let sum: i64 = numbers.iter().sum();
    let sum_squares: i64 = numbers.iter().map(|x| x * x).sum();
    let max_val = numbers.iter().max().unwrap();
    let min_val = numbers.iter().min().unwrap();
    let average = sum as f64 / numbers.len() as f64;
    
    dict.set_item("sum_squares", sum_squares)?;
    dict.set_item("sum", sum)?;
    dict.set_item("max", *max_val)?;
    dict.set_item("min", *min_val)?;
    dict.set_item("average", average)?;
    
    Ok(dict.into())
}

/// Вычисление числа Фибоначчи (итеративно)
#[pyfunction]
fn fibonacci(n: u64) -> u64 {
    if n <= 1 {
        return n;
    }
    let mut a = 0;
    let mut b = 1;
    for _ in 1..n {
        let temp = a + b;
        a = b;
        b = temp;
    }
    b
}

/// Тяжелые вычисления для профилирования
#[pyfunction]
fn heavy_computation(py: Python, numbers: Vec<i64>) -> PyResult<PyObject> {
    let dict = PyDict::new(py);
    
    let sum_squares: i64 = numbers.iter().map(|x| x * x).sum();
    let fib_30 = fibonacci(30);
    
    dict.set_item("sum_squares", sum_squares)?;
    dict.set_item("fibonacci_30", fib_30)?;
    dict.set_item("processed_length", numbers.len())?;
    
    Ok(dict.into())
}

/// Python модуль
#[pymodule]
fn fastmath(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_squares, m)?)?;
    m.add_function(wrap_pyfunction!(process_numbers, m)?)?;
    m.add_function(wrap_pyfunction!(fibonacci, m)?)?;
    m.add_function(wrap_pyfunction!(heavy_computation, m)?)?;
    Ok(())
}