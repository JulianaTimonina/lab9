"""Unit tests for Rust-based fastmath module."""

import unittest
import sys
import os

# Добавляем корневую директорию для импорта fastmath
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

try:
    import fastmath
    RUST_AVAILABLE = True
except ImportError as e:
    RUST_AVAILABLE = False
    print(f"Rust module not available: {e}")


def dict_from_pairs(pairs):
    """Convert list of tuples to dictionary."""
    return {key: value for key, value in pairs}


@unittest.skipUnless(RUST_AVAILABLE, "Rust module not available")
class TestRustCalculator(unittest.TestCase):
    """Test cases for Rust implementation."""
    
    def test_sum_squares(self):
        """Test sum of squares function."""
        self.assertEqual(fastmath.sum_squares([1, 2, 3]), 14)
        self.assertEqual(fastmath.sum_squares([]), 0)
        self.assertEqual(fastmath.sum_squares([5]), 25)
        self.assertEqual(fastmath.sum_squares([-2, 3]), 13)
    
    def test_process_numbers(self):
        """Test complete number processing."""
        # Rust возвращает список пар [("key", value), ...]
        result_list = fastmath.process_numbers([1, 2, 3, 4, 5])
        
        # Преобразуем в словарь для удобства проверки
        result = dict_from_pairs(result_list)
        
        self.assertEqual(result["sum"], 15)
        self.assertEqual(result["sum_squares"], 55)
        self.assertEqual(result["max"], 5)
        self.assertEqual(result["min"], 1)
        self.assertEqual(result["average"], 3.0)
    
    def test_process_numbers_empty(self):
        """Test processing empty list."""
        result_list = fastmath.process_numbers([])
        result = dict_from_pairs(result_list)
        
        self.assertEqual(result["sum"], 0)
        self.assertEqual(result["sum_squares"], 0)
        # Rust возвращает 0 для пустого списка вместо None
        self.assertEqual(result["max"], 0)
        self.assertEqual(result["min"], 0)
        self.assertEqual(result["average"], 0.0)
    
    def test_fibonacci(self):
        """Test Fibonacci function."""
        self.assertEqual(fastmath.fibonacci(0), 0)
        self.assertEqual(fastmath.fibonacci(1), 1)
        self.assertEqual(fastmath.fibonacci(2), 1)
        self.assertEqual(fastmath.fibonacci(3), 2)
        self.assertEqual(fastmath.fibonacci(10), 55)
        self.assertEqual(fastmath.fibonacci(30), 832040)
    
    def test_heavy_computation(self):
        """Test heavy computation function."""
        result_list = fastmath.heavy_computation([1, 2, 3])
        result = dict_from_pairs(result_list)
        
        self.assertEqual(result["sum_squares"], 14)
        self.assertEqual(result["fibonacci_30"], 832040)
        self.assertEqual(result["processed_length"], 3)


if __name__ == "__main__":
    unittest.main()