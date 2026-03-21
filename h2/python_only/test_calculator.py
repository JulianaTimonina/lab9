"""Unit tests for Python-only calculator."""

import unittest
import sys
import os

# Добавляем текущую директорию в путь
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from calculator import (
    sum_squares_python,
    process_numbers_python,
    fibonacci_iterative_python,
    heavy_computation_python
)


class TestPythonCalculator(unittest.TestCase):
    """Test cases for Python implementation."""
    
    def test_sum_squares(self):
        """Test sum of squares function."""
        self.assertEqual(sum_squares_python([1, 2, 3]), 14)
        self.assertEqual(sum_squares_python([]), 0)
        self.assertEqual(sum_squares_python([5]), 25)
        self.assertEqual(sum_squares_python([-2, 3]), 13)
    
    def test_process_numbers(self):
        """Test complete number processing."""
        result = process_numbers_python([1, 2, 3, 4, 5])
        self.assertEqual(result["sum"], 15)
        self.assertEqual(result["sum_squares"], 55)
        self.assertEqual(result["max"], 5)
        self.assertEqual(result["min"], 1)
        self.assertEqual(result["average"], 3.0)
    
    def test_process_numbers_empty(self):
        """Test processing empty list."""
        result = process_numbers_python([])
        self.assertEqual(result["sum"], 0)
        self.assertEqual(result["sum_squares"], 0)
        self.assertIsNone(result["max"])
        self.assertIsNone(result["min"])
        self.assertEqual(result["average"], 0)
    
    def test_fibonacci(self):
        """Test Fibonacci function."""
        self.assertEqual(fibonacci_iterative_python(0), 0)
        self.assertEqual(fibonacci_iterative_python(1), 1)
        self.assertEqual(fibonacci_iterative_python(2), 1)
        self.assertEqual(fibonacci_iterative_python(3), 2)
        self.assertEqual(fibonacci_iterative_python(10), 55)
        self.assertEqual(fibonacci_iterative_python(30), 832040)
    
    def test_heavy_computation(self):
        """Test heavy computation function."""
        result = heavy_computation_python([1, 2, 3])
        self.assertEqual(result["sum_squares"], 14)
        self.assertEqual(result["fibonacci_30"], 832040)
        self.assertEqual(result["processed_length"], 3)


if __name__ == "__main__":
    unittest.main()