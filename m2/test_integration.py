import unittest
import json
import subprocess
import os

class TestGoCalculator(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Подготовка перед тестами"""
        cls.binary_path = "./calculator"
        
        # Проверяем существование бинарного файла
        if not os.path.exists(cls.binary_path):
            raise unittest.SkipTest(f"Go binary not found at {cls.binary_path}")
    
    def test_basic_numbers(self):
        """Тест с базовыми числами"""
        # Подготавливаем данные
        input_data = {"numbers": [1, 2, 3, 4, 5]}
        
        # Запускаем Go процесс
        proc = subprocess.Popen(
            [self.binary_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, _ = proc.communicate(json.dumps(input_data).encode())
        result = json.loads(stdout.decode())
        
        # Проверяем результат
        self.assertEqual(result['sum'], 15)
        self.assertEqual(result['square_sum'], 55)
        self.assertEqual(result['processed'], [1, 4, 9, 16, 25])
        self.assertEqual(result['status'], 'success')
    
    def test_negative_numbers(self):
        """Тест с отрицательными числами"""
        input_data = {"numbers": [-1, -2, -3]}
        
        proc = subprocess.Popen(
            [self.binary_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, _ = proc.communicate(json.dumps(input_data).encode())
        result = json.loads(stdout.decode())
        
        self.assertEqual(result['sum'], -6)
        self.assertEqual(result['square_sum'], 14)
        self.assertEqual(result['processed'], [1, 4, 9])
    
    def test_empty_list(self):
        """Тест с пустым списком"""
        input_data = {"numbers": []}
        
        proc = subprocess.Popen(
            [self.binary_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, _ = proc.communicate(json.dumps(input_data).encode())
        result = json.loads(stdout.decode())
        
        self.assertEqual(result['sum'], 0)
        self.assertEqual(result['square_sum'], 0)
        self.assertEqual(result['processed'], [])
    
    def test_single_number(self):
        """Тест с одним числом"""
        input_data = {"numbers": [42]}
        
        proc = subprocess.Popen(
            [self.binary_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, _ = proc.communicate(json.dumps(input_data).encode())
        result = json.loads(stdout.decode())
        
        self.assertEqual(result['sum'], 42)
        self.assertEqual(result['square_sum'], 1764)
        self.assertEqual(result['processed'], [1764])
    
    def test_large_numbers(self):
        """Тест с большими числами"""
        input_data = {"numbers": [1000, 2000, 3000]}
        
        proc = subprocess.Popen(
            [self.binary_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, _ = proc.communicate(json.dumps(input_data).encode())
        result = json.loads(stdout.decode())
        
        self.assertEqual(result['sum'], 6000)
        self.assertEqual(result['square_sum'], 1000000 + 4000000 + 9000000)
    
    def test_zero(self):
        """Тест с нулём"""
        input_data = {"numbers": [0, 0, 0]}
        
        proc = subprocess.Popen(
            [self.binary_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, _ = proc.communicate(json.dumps(input_data).encode())
        result = json.loads(stdout.decode())
        
        self.assertEqual(result['sum'], 0)
        self.assertEqual(result['square_sum'], 0)
        self.assertEqual(result['processed'], [0, 0, 0])
    
    def test_invalid_binary_path(self):
        """Тест с неверным путём к бинарю"""
        with self.assertRaises(FileNotFoundError):
            from main import GoCalculator
            calculator = GoCalculator("/nonexistent/path")

if __name__ == "__main__":
    unittest.main()