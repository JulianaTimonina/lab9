import unittest
import random
import rust_math

class TestRustMath(unittest.TestCase):
    """Тесты для Rust модуля"""
    
    def test_sum_squares(self):
        """Тест суммы квадратов"""
        numbers = [1, 2, 3, 4, 5]
        result = rust_math.sum_squares(numbers)
        self.assertEqual(result, 55)
    
    def test_product(self):
        """Тест произведения"""
        numbers = [1, 2, 3, 4, 5]
        result = rust_math.product(numbers)
        self.assertEqual(result, 120)
    
    def test_calculate_all(self):
        """Тест всех вычислений"""
        numbers = [1, 2, 3, 4, 5]
        sum_val, product, square_sum = rust_math.calculate_all(numbers)
        self.assertEqual(sum_val, 15)
        self.assertEqual(product, 120)
        self.assertEqual(square_sum, 55)
    
    def test_fibonacci_recursive(self):
        """Тест рекурсивного Фибоначчи"""
        self.assertEqual(rust_math.fibonacci_recursive(0), 0)
        self.assertEqual(rust_math.fibonacci_recursive(1), 1)
        self.assertEqual(rust_math.fibonacci_recursive(10), 55)
        self.assertEqual(rust_math.fibonacci_recursive(20), 6765)
    
    def test_fibonacci_iterative(self):
        """Тест итеративного Фибоначчи"""
        self.assertEqual(rust_math.fibonacci_iterative(0), 0)
        self.assertEqual(rust_math.fibonacci_iterative(1), 1)
        self.assertEqual(rust_math.fibonacci_iterative(10), 55)
        self.assertEqual(rust_math.fibonacci_iterative(20), 6765)
    
    def test_sort_numbers(self):
        """Тест сортировки"""
        numbers = [5, 2, 8, 1, 9, 3]
        sorted_numbers = rust_math.sort_numbers(numbers)
        self.assertEqual(sorted_numbers, [1, 2, 3, 5, 8, 9])
        
        # Проверка на пустом списке
        empty = rust_math.sort_numbers([])
        self.assertEqual(empty, [])
        
        # Проверка с отрицательными числами
        negative = rust_math.sort_numbers([-5, 0, -2, 3, -1])
        self.assertEqual(negative, [-5, -2, -1, 0, 3])
    
    def test_filter_even(self):
        """Тест фильтрации чётных чисел"""
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        even = rust_math.filter_even(numbers)
        self.assertEqual(even, [2, 4, 6, 8, 10])
        
        # Проверка с пустым списком
        empty = rust_math.filter_even([])
        self.assertEqual(empty, [])
        
        # Проверка с отрицательными числами
        negative = rust_math.filter_even([-5, -4, -3, -2, -1, 0])
        self.assertEqual(negative, [-4, -2, 0])
    
    def test_large_numbers(self):
        """Тест с большими числами"""
        numbers = list(range(10000))
        result_rust = rust_math.sum_squares(numbers)
        
        # Проверяем, что Rust не падает с большими данными
        self.assertIsInstance(result_rust, int)

if __name__ == "__main__":
    unittest.main()