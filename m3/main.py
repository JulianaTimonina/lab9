import time
import sys
import random

# Импортируем Rust модуль
try:
    import rust_math
    RUST_AVAILABLE = True
except ImportError:
    print("Rust module not found. Please install with: pip install .")
    RUST_AVAILABLE = False
    sys.exit(1)

# Python реализации для сравнения
def sum_squares_python(numbers):
    """Python реализация суммы квадратов"""
    return sum(x * x for x in numbers)

def product_python(numbers):
    """Python реализация произведения"""
    result = 1
    for x in numbers:
        result *= x
    return result

def fibonacci_recursive_python(n):
    """Python рекурсивный Фибоначчи"""
    if n <= 1:
        return n
    return fibonacci_recursive_python(n - 1) + fibonacci_recursive_python(n - 2)

def fibonacci_iterative_python(n):
    """Python итеративный Фибоначчи"""
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr

def sort_numbers_python(numbers):
    """Python сортировка"""
    return sorted(numbers)

def filter_even_python(numbers):
    """Python фильтрация чётных"""
    return [x for x in numbers if x % 2 == 0]

def measure_time(func, *args, iterations=100):
    """Измеряет время выполнения функции"""
    # Прогрев
    for _ in range(min(3, iterations)):
        try:
            func(*args)
        except:
            pass
    
    # Замер времени
    start = time.perf_counter()
    for _ in range(iterations):
        try:
            result = func(*args)
        except:
            result = None
    end = time.perf_counter()
    
    return end - start, result

def run_comparison():
    """Запускает сравнение производительности"""
    print("=" * 60)
    print("Сравнение производительности Rust vs Python")
    print("=" * 60)
    
    results = []
    
    # Тест 1: Сумма квадратов
    print("\n1. Сумма квадратов:")
    test_data = [
        ("50 элементов", list(range(50)), 1000),
        ("500 элементов", list(range(500)), 500),
    ]
    
    for name, data, iterations in test_data:
        rust_time, rust_result = measure_time(rust_math.sum_squares, data, iterations=iterations)
        py_time, py_result = measure_time(sum_squares_python, data, iterations=iterations)
        speedup = py_time / rust_time if rust_time > 0 else 0
        
        print(f"  {name} ({iterations} итераций):")
        print(f"    Rust: {rust_time:.4f} сек")
        print(f"    Python: {py_time:.4f} сек")
        print(f"    Ускорение: {speedup:.2f}x")
        print(f"    Результаты совпадают: {rust_result == py_result}")
        
        results.append({
            'test': f'Сумма квадратов ({name})',
            'rust_time': rust_time,
            'python_time': py_time,
            'speedup': speedup,
            'match': rust_result == py_result
        })
    
    # Тест 2: Произведение
    print("\n2. Произведение:")
    product_data = list(range(1, 21))
    iterations = 500
    
    rust_time, rust_result = measure_time(rust_math.product, product_data, iterations=iterations)
    py_time, py_result = measure_time(product_python, product_data, iterations=iterations)
    speedup = py_time / rust_time if rust_time > 0 else 0
    
    print(f"  {len(product_data)} элементов ({iterations} итераций):")
    print(f"    Rust: {rust_time:.4f} сек")
    print(f"    Python: {py_time:.4f} сек")
    print(f"    Ускорение: {speedup:.2f}x")
    print(f"    Результаты совпадают: {rust_result == py_result}")
    
    results.append({
        'test': 'Произведение',
        'rust_time': rust_time,
        'python_time': py_time,
        'speedup': speedup,
        'match': rust_result == py_result
    })
    
    # Тест 3: Фибоначчи рекурсивный
    print("\n3. Фибоначчи (рекурсивный):")
    n = 30
    iterations = 5
    
    rust_time, rust_result = measure_time(rust_math.fibonacci_recursive, n, iterations=iterations)
    py_time, py_result = measure_time(fibonacci_recursive_python, n, iterations=iterations)
    speedup = py_time / rust_time if rust_time > 0 else 0
    
    print(f"  n={n} ({iterations} итераций):")
    print(f"    Rust: {rust_time:.4f} сек")
    print(f"    Python: {py_time:.4f} сек")
    print(f"    Ускорение: {speedup:.2f}x")
    print(f"    Результаты совпадают: {rust_result == py_result}")
    
    results.append({
        'test': f'Фибоначчи рекурсивный (n={n})',
        'rust_time': rust_time,
        'python_time': py_time,
        'speedup': speedup,
        'match': rust_result == py_result
    })
    
    # Тест 4: Фибоначчи итеративный
    print("\n4. Фибоначчи (итеративный):")
    n = 50
    iterations = 10
    
    rust_time, rust_result = measure_time(rust_math.fibonacci_iterative, n, iterations=iterations)
    py_time, py_result = measure_time(fibonacci_iterative_python, n, iterations=iterations)
    speedup = py_time / rust_time if rust_time > 0 else 0
    
    print(f"  n={n} ({iterations} итераций):")
    print(f"    Rust: {rust_time:.4f} сек")
    print(f"    Python: {py_time:.4f} сек")
    print(f"    Ускорение: {speedup:.2f}x")
    print(f"    Результаты совпадают: {rust_result == py_result}")
    
    results.append({
        'test': f'Фибоначчи итеративный (n={n})',
        'rust_time': rust_time,
        'python_time': py_time,
        'speedup': speedup,
        'match': rust_result == py_result
    })
    
    # Тест 5: Сортировка
    print("\n5. Сортировка:")
    sort_size = 10000
    iterations = 10
    sort_data = [random.randint(0, sort_size) for _ in range(sort_size)]
    
    rust_time, rust_result = measure_time(rust_math.sort_numbers, sort_data.copy(), iterations=iterations)
    py_time, py_result = measure_time(sort_numbers_python, sort_data.copy(), iterations=iterations)
    speedup = py_time / rust_time if rust_time > 0 else 0
    
    print(f"  {sort_size} элементов ({iterations} итераций):")
    print(f"    Rust: {rust_time:.4f} сек")
    print(f"    Python: {py_time:.4f} сек")
    print(f"    Ускорение: {speedup:.2f}x")
    print(f"    Результаты совпадают: {rust_result == py_result}")
    
    results.append({
        'test': f'Сортировка ({sort_size} элементов)',
        'rust_time': rust_time,
        'python_time': py_time,
        'speedup': speedup,
        'match': rust_result == py_result
    })
    
    # Тест 6: Фильтрация чётных
    print("\n6. Фильтрация чётных:")
    filter_size = 100000
    iterations = 10
    filter_data = [random.randint(0, 1000) for _ in range(filter_size)]
    
    rust_time, rust_result = measure_time(rust_math.filter_even, filter_data.copy(), iterations=iterations)
    py_time, py_result = measure_time(filter_even_python, filter_data.copy(), iterations=iterations)
    speedup = py_time / rust_time if rust_time > 0 else 0
    
    print(f"  {filter_size} элементов ({iterations} итераций):")
    print(f"    Rust: {rust_time:.4f} сек")
    print(f"    Python: {py_time:.4f} сек")
    print(f"    Ускорение: {speedup:.2f}x")
    print(f"    Результаты совпадают: {len(rust_result) == len(py_result)}")
    
    results.append({
        'test': f'Фильтрация чётных ({filter_size} элементов)',
        'rust_time': rust_time,
        'python_time': py_time,
        'speedup': speedup,
        'match': len(rust_result) == len(py_result)
    })
    
    # Вывод итоговой статистики
    print("\n" + "=" * 60)
    print("ИТОГОВАЯ СТАТИСТИКА")
    print("=" * 60)
    
    avg_speedup = sum(r['speedup'] for r in results) / len(results)
    max_speedup = max(r['speedup'] for r in results)
    min_speedup = min(r['speedup'] for r in results)
    matches = sum(1 for r in results if r['match'])
    
    print(f"Среднее ускорение: {avg_speedup:.2f}x")
    print(f"Максимальное ускорение: {max_speedup:.2f}x")
    print(f"Минимальное ускорение: {min_speedup:.2f}x")
    print(f"Совпадение результатов: {matches}/{len(results)} тестов")
    print(f"Всего тестов: {len(results)}")
    
    # Детальный отчёт по тестам
    print("\n" + "=" * 60)
    print("ДЕТАЛЬНЫЙ ОТЧЁТ ПО ТЕСТАМ")
    print("=" * 60)
    for r in results:
        status = "✓" if r['match'] else "✗"
        print(f"{status} {r['test']}: {r['speedup']:.2f}x ускорение")

if __name__ == "__main__":
    run_comparison()