import subprocess
import json
import os

class GoCalculator:
    """Класс для взаимодействия с Go-бинарём через подпроцесс"""
    
    def __init__(self, binary_path="./calculator"):
        """
        Инициализация калькулятора
        
        Args:
            binary_path (str): Путь к скомпилированному Go-бинарю
        """
        if not os.path.exists(binary_path):
            raise FileNotFoundError(f"Go binary not found at {binary_path}")
        self.binary_path = binary_path
    
    def process_numbers(self, numbers):
        """
        Отправляет числа в Go-программу и получает результат
        
        Args:
            numbers (list): Список целых чисел
            
        Returns:
            dict: Результат вычислений
        """
        # Формируем входные данные
        input_data = {"numbers": numbers}
        input_json = json.dumps(input_data)
        
        # Запускаем Go-процесс
        proc = subprocess.Popen(
            [self.binary_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Передаём данные и получаем результат
        stdout, stderr = proc.communicate(input_json.encode('utf-8'))
        
        if stderr:
            print(f"Warning from Go process: {stderr.decode()}")
        
        # Парсим результат
        try:
            result = json.loads(stdout.decode('utf-8'))
            return result
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Go response: {e}")

def main():
    """Пример использования"""
    # Создаём экземпляр калькулятора
    calculator = GoCalculator()
    
    # Тестовые данные
    test_cases = [
        [1, 2, 3, 4, 5],
        [10, 20, 30],
        [0, -1, -2],
        [100]
    ]
    
    # Обрабатываем каждый тест
    for numbers in test_cases:
        print(f"\nInput: {numbers}")
        try:
            result = calculator.process_numbers(numbers)
            print(f"  Sum: {result['sum']}")
            print(f"  Square Sum: {result['square_sum']}")
            print(f"  Processed: {result['processed']}")
            print(f"  Status: {result['status']}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    main()