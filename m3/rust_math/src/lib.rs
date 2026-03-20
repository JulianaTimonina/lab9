use pyo3::prelude::*;

/// Вычисляет сумму квадратов чисел
#[pyfunction]
fn sum_squares(numbers: Vec<i64>) -> i64 {
    numbers.iter().map(|x| x * x).sum()
}

/// Вычисляет произведение всех чисел
#[pyfunction]
fn product(numbers: Vec<i64>) -> i64 {
    numbers.iter().product()
}

/// Вычисляет сумму, произведение и сумму квадратов за один проход
#[pyfunction]
fn calculate_all(numbers: Vec<i64>) -> (i64, i64, i64) {
    let mut sum = 0;
    let mut product = 1;
    let mut square_sum = 0;
    
    for &n in &numbers {
        sum += n;
        product *= n;
        square_sum += n * n;
    }
    
    (sum, product, square_sum)
}

/// Фибоначчи (рекурсивно) - для тестирования производительности
#[pyfunction]
fn fibonacci_recursive(n: u64) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2),
    }
}

/// Фибоначчи (итеративно) - для тестирования производительности
#[pyfunction]
fn fibonacci_iterative(n: u64) -> u64 {
    if n == 0 {
        return 0;
    }
    if n == 1 {
        return 1;
    }
    
    let mut prev = 0;
    let mut curr = 1;
    
    for _ in 2..=n {
        let next = prev + curr;
        prev = curr;
        curr = next;
    }
    
    curr
}

/// Сортировка списка
#[pyfunction]
fn sort_numbers(mut numbers: Vec<i64>) -> Vec<i64> {
    numbers.sort();
    numbers
}

/// Фильтрация чётных чисел
#[pyfunction]
fn filter_even(numbers: Vec<i64>) -> Vec<i64> {
    numbers.into_iter().filter(|&x| x % 2 == 0).collect()
}

/// Модуль для Python
#[pymodule]
fn rust_math(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_squares, m)?)?;
    m.add_function(wrap_pyfunction!(product, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_all, m)?)?;
    m.add_function(wrap_pyfunction!(fibonacci_recursive, m)?)?;
    m.add_function(wrap_pyfunction!(fibonacci_iterative, m)?)?;
    m.add_function(wrap_pyfunction!(sort_numbers, m)?)?;
    m.add_function(wrap_pyfunction!(filter_even, m)?)?;
    Ok(())
}