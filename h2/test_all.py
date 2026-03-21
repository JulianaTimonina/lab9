"""Run all tests for all implementations."""

import unittest
import sys
import os

# Добавляем все пути
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "python_only"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "rust_lib"))

# Импортируем тесты
from python_only.test_calculator import TestPythonCalculator

try:
    from rust_lib.test_fastmath import TestRustCalculator
    RUST_TESTS_AVAILABLE = True
except ImportError as e:
    RUST_TESTS_AVAILABLE = False
    print(f"⚠️  Rust tests not available: {e}")

try:
    from go_service.test_go_service import TestGoService
    GO_TESTS_AVAILABLE = True
except ImportError as e:
    GO_TESTS_AVAILABLE = False
    print(f"⚠️  Go tests not available: {e}")


def run_all_tests():
    """Run all test suites."""
    print("=" * 60)
    print("RUNNING ALL TESTS")
    print("=" * 60)
    
    # Создаем загрузчик тестов
    loader = unittest.TestLoader()
    
    # Добавляем тесты
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestPythonCalculator))
    
    if RUST_TESTS_AVAILABLE:
        try:
            suite.addTests(loader.loadTestsFromTestCase(TestRustCalculator))
        except Exception as e:
            print(f"⚠️  Failed to load Rust tests: {e}")
    
    if GO_TESTS_AVAILABLE:
        try:
            # Проверяем Go сервер
            import requests
            try:
                requests.get("http://localhost:8080/health", timeout=1)
                suite.addTests(loader.loadTestsFromTestCase(TestGoService))
            except:
                print("⚠️  Go server not available, skipping Go tests")
        except ImportError:
            print("⚠️  Requests module not available, skipping Go tests")
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим итоги
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)