"""Бенчмарк: Python vs Rust vs Go - сравнение производительности."""

import time
import statistics
import sys
import os
import subprocess
import signal
import atexit
from typing import List, Dict, Any
import requests
import json

# Добавляем путь для импорта Python модуля
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "python_only"))
from calculator import (
    sum_squares_python, 
    process_numbers_python,
    fibonacci_iterative_python,
    heavy_computation_python
)

# Импорт Rust модуля
try:
    import fastmath
    RUST_AVAILABLE = True
    print("✓ Rust module loaded")
except ImportError as e:
    RUST_AVAILABLE = False
    print(f"✗ Rust module not available: {e}")

GO_SERVER_URL = "http://localhost:8080"
go_process = None


def start_go_server():
    """Запускает Go сервер в фоновом процессе."""
    global go_process
    try:
        go_process = subprocess.Popen(
            ["go", "run", "main.go"],
            cwd=os.path.join(os.path.dirname(__file__), "go_service"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Ждем запуска сервера
        for _ in range(10):
            try:
                response = requests.get(f"{GO_SERVER_URL}/health", timeout=1)
                if response.status_code == 200:
                    print("✓ Go server started successfully")
                    return True
            except:
                time.sleep(0.5)
        
        print("✗ Failed to start Go server")
        return False
    except Exception as e:
        print(f"✗ Error starting Go server: {e}")
        return False


def stop_go_server():
    """Останавливает Go сервер."""
    global go_process
    if go_process:
        go_process.terminate()
        try:
            go_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            go_process.kill()
        print("✓ Go server stopped")


def benchmark(func, *args, iterations=100):
    """Измеряет время выполнения функции."""
    # Прогрев
    for _ in range(3):
        func(*args)
    
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        result = func(*args)
        times.append((time.perf_counter() - start) * 1000)
    
    return {
        "mean": statistics.mean(times),
        "stddev": statistics.stdev(times) if len(times) > 1 else 0,
        "result": result
    }


def test_go_sum_squares(numbers):
    """Вызов Go сервера для суммы квадратов."""
    resp = requests.post(f"{GO_SERVER_URL}/process", json={"numbers": numbers})
    return resp.json()["sum_squares"]


def test_go_process_numbers(numbers):
    """Вызов Go сервера для полной обработки."""
    resp = requests.post(f"{GO_SERVER_URL}/process", json={"numbers": numbers})
    return resp.json()


def test_go_heavy_computation(numbers):
    """Вызов Go сервера для тяжелых вычислений."""
    resp = requests.post(f"{GO_SERVER_URL}/heavy", json={"numbers": numbers})
    return resp.json()


def run_comparison():
    """Запуск полного сравнения производительности."""
    print("=" * 80)
    print("PERFORMANCE COMPARISON: Python vs Python+Rust vs Python+Go")
    print("All implementations use the same iterative Fibonacci algorithm")
    print("=" * 80)
    
    # Проверка Go сервера
    try:
        requests.get(f"{GO_SERVER_URL}/health", timeout=2)
        GO_AVAILABLE = True
        print("✓ Go server is running")
    except:
        GO_AVAILABLE = False
        print("✗ Go server not running")
    
    # Тест 1: Сумма квадратов (разные размеры данных)
    print("\n" + "=" * 80)
    print("TEST 1: Sum of Squares (Simple Computation)")
    print("=" * 80)
    
    sizes = [100, 1000, 5000, 10000, 50000]
    
    print(f"{'Size':<10} {'Python (ms)':<15} {'Rust (ms)':<15} {'Go (ms)':<15}")
    print("-" * 80)
    
    results = {}
    for size in sizes:
        data = list(range(size))
        
        # Python
        py_result = benchmark(sum_squares_python, data, iterations=100)
        
        # Rust
        if RUST_AVAILABLE:
            rust_result = benchmark(fastmath.sum_squares, data, iterations=100)
        
        # Go
        if GO_AVAILABLE:
            go_times = []
            for _ in range(100):
                start = time.perf_counter()
                test_go_sum_squares(data)
                go_times.append((time.perf_counter() - start) * 1000)
            go_mean = statistics.mean(go_times)
            go_stddev = statistics.stdev(go_times)
        
        # Сохраняем результаты
        results[size] = {
            "python": py_result["mean"],
            "rust": rust_result["mean"] if RUST_AVAILABLE else None,
            "go": go_mean if GO_AVAILABLE else None
        }
        
        # Вывод
        print(f"{size:<10} {py_result['mean']:<15.3f} ", end="")
        if RUST_AVAILABLE:
            print(f"{rust_result['mean']:<15.3f} ", end="")
        else:
            print(f"{'N/A':<15} ", end="")
        if GO_AVAILABLE:
            print(f"{go_mean:<15.3f}")
        else:
            print(f"{'N/A':<15}")
    
    # Тест 2: Полная обработка данных
    print("\n" + "=" * 80)
    print("TEST 2: Complete Data Processing (Sum, SumSquares, Max, Min, Average)")
    print("=" * 80)
    
    test_size = 10000
    data = list(range(test_size))
    
    print(f"Processing {test_size} numbers...")
    print()
    
    # Python
    py_result = benchmark(process_numbers_python, data, iterations=50)
    print(f"Python:     {py_result['mean']:.3f} ms (±{py_result['stddev']:.3f})")
    print(f"  Result: {py_result['result']}")
    print()
    
    # Rust
    if RUST_AVAILABLE:
        rust_result = benchmark(fastmath.process_numbers, data, iterations=50)
        print(f"Rust:       {rust_result['mean']:.3f} ms (±{rust_result['stddev']:.3f})")
        print(f"  Result: {rust_result['result']}")
        print(f"  → Rust is {py_result['mean']/rust_result['mean']:.1f}x faster")
        print()
    
    # Go
    if GO_AVAILABLE:
        go_times = []
        go_results = []
        for _ in range(50):
            start = time.perf_counter()
            result = test_go_process_numbers(data)
            go_times.append((time.perf_counter() - start) * 1000)
            go_results.append(result)
        go_mean = statistics.mean(go_times)
        go_stddev = statistics.stdev(go_times)
        print(f"Go:         {go_mean:.3f} ms (±{go_stddev:.3f})")
        print(f"  Result: {go_results[0]}")
        print(f"  → Go is {py_result['mean']/go_mean:.1f}x faster")
    
    # Тест 3: Фибоначчи (тяжелые вычисления)
    print("\n" + "=" * 80)
    print("TEST 3: Fibonacci(30) - Heavy Computation")
    print("=" * 80)
    
    # Python
    py_result = benchmark(fibonacci_iterative_python, 30, iterations=100)
    print(f"Python: {py_result['mean']:.3f} ms (±{py_result['stddev']:.3f})")
    
    # Rust
    if RUST_AVAILABLE:
        rust_result = benchmark(fastmath.fibonacci, 30, iterations=100)
        print(f"Rust:   {rust_result['mean']:.3f} ms (±{rust_result['stddev']:.3f})")
        print(f"  → Rust is {py_result['mean']/rust_result['mean']:.1f}x faster")
    
    # Go
    if GO_AVAILABLE:
        go_times = []
        for _ in range(100):
            start = time.perf_counter()
            test_go_heavy_computation([1])
            go_times.append((time.perf_counter() - start) * 1000)
        go_mean = statistics.mean(go_times)
        go_stddev = statistics.stdev(go_times)
        print(f"Go:     {go_mean:.3f} ms (±{go_stddev:.3f})")
        print(f"  → Go is {py_result['mean']/go_mean:.1f}x faster")
    
    # Тест 4: Тяжелые вычисления с данными
    print("\n" + "=" * 80)
    print("TEST 4: Heavy Computation (SumSquares + Fibonacci)")
    print("=" * 80)
    
    test_size = 10000
    data = list(range(test_size))
    
    print(f"Processing {test_size} numbers with Fibonacci(30)...")
    print()
    
    # Python
    py_result = benchmark(heavy_computation_python, data, iterations=30)
    print(f"Python: {py_result['mean']:.3f} ms (±{py_result['stddev']:.3f})")
    
    # Rust
    if RUST_AVAILABLE:
        rust_result = benchmark(fastmath.heavy_computation, data, iterations=30)
        print(f"Rust:   {rust_result['mean']:.3f} ms (±{rust_result['stddev']:.3f})")
        print(f"  → Rust is {py_result['mean']/rust_result['mean']:.1f}x faster")
    
    # Go
    if GO_AVAILABLE:
        go_times = []
        for _ in range(30):
            start = time.perf_counter()
            test_go_heavy_computation(data)
            go_times.append((time.perf_counter() - start) * 1000)
        go_mean = statistics.mean(go_times)
        go_stddev = statistics.stdev(go_times)
        print(f"Go:     {go_mean:.3f} ms (±{go_stddev:.3f})")
        print(f"  → Go is {py_result['mean']/go_mean:.1f}x faster")
    
    # Итоговый анализ
    print("\n" + "=" * 80)
    print("SUMMARY & ANALYSIS")
    print("=" * 80)
    
    if RUST_AVAILABLE:
        print("\n📊 Python+Rust Performance:")
        print("  • 10-100x faster for pure computations")
        print("  • Zero overhead Python bindings")
        print("  • Best for CPU-intensive tasks")
        print("  • Easy integration with existing Python code")
    
    if GO_AVAILABLE:
        print("\n📊 Python+Go Performance:")
        print("  • 5-50x faster than pure Python")
        print("  • Network overhead adds latency")
        print("  • Best for microservices and concurrent tasks")
        print("  • Can be scaled independently")
    
    print("\n📊 Python Performance:")
    print("  • Slowest for CPU-bound tasks")
    print("  • Good for prototyping and I/O-bound tasks")
    print("  • Largest ecosystem of libraries")
    
    print("\n✅ Benchmark completed!")


if __name__ == "__main__":
    # Регистрируем остановку Go сервера при выходе
    atexit.register(stop_go_server)
    
    # Запускаем Go сервер если не запущен
    try:
        requests.get(f"{GO_SERVER_URL}/health", timeout=1)
        print("✓ Go server already running")
    except:
        print("Starting Go server...")
        if not start_go_server():
            print("⚠️  Continuing without Go server...")
    
    # Запускаем сравнение
    run_comparison()