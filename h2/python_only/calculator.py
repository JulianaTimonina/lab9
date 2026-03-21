"""Чистая реализация на Python для сравнения производительности."""

from typing import List, Dict, Any


def sum_squares_python(numbers: List[int]) -> int:
    """Вычисление суммы квадратов чисел."""
    return sum(x * x for x in numbers)


def process_numbers_python(numbers: List[int]) -> Dict[str, Any]:
    """Обработка списка чисел с различными операциями."""
    if not numbers:
        return {
            "sum_squares": 0,
            "sum": 0,
            "max": None,
            "min": None,
            "average": 0.0,
        }
    
    total_sum = sum(numbers)
    return {
        "sum_squares": sum_squares_python(numbers),
        "sum": total_sum,
        "max": max(numbers),
        "min": min(numbers),
        "average": total_sum / len(numbers),
    }


def fibonacci_iterative_python(n: int) -> int:
    """Вычисление числа Фибоначчи (итеративно, для равного сравнения)."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(1, n):
        a, b = b, a + b
    return b


def heavy_computation_python(numbers: List[int]) -> Dict[str, Any]:
    """Тяжелые вычисления для профилирования."""
    return {
        "sum_squares": sum_squares_python(numbers),
        "fibonacci_30": fibonacci_iterative_python(30),
        "processed_length": len(numbers),
    }