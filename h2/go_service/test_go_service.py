"""Unit tests for Go HTTP service."""

import unittest
import requests
import json
import time
import subprocess
import os
import sys


class TestGoService(unittest.TestCase):
    """Test cases for Go service."""
    
    @classmethod
    def setUpClass(cls):
        """Start Go server before all tests."""
        cls.server_url = "http://localhost:8080"
        cls.process = None
        
        # Проверяем, запущен ли сервер
        try:
            response = requests.get(f"{cls.server_url}/health", timeout=1)
            if response.status_code == 200:
                print("✓ Go server already running")
                return
        except:
            pass
        
        # Запускаем сервер
        print("Starting Go server...")
        go_dir = os.path.dirname(__file__)
        cls.process = subprocess.Popen(
            ["go", "run", "main.go"],
            cwd=go_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Ждем запуска
        for _ in range(10):
            try:
                requests.get(f"{cls.server_url}/health", timeout=1)
                print("✓ Go server started")
                return
            except:
                time.sleep(0.5)
        
        raise RuntimeError("Failed to start Go server")
    
    @classmethod
    def tearDownClass(cls):
        """Stop Go server after all tests."""
        if cls.process:
            cls.process.terminate()
            cls.process.wait(timeout=5)
            print("✓ Go server stopped")
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = requests.get(f"{self.server_url}/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
    
    def test_process_numbers(self):
        """Test process endpoint."""
        payload = {"numbers": [1, 2, 3, 4, 5]}
        response = requests.post(f"{self.server_url}/process", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["sum"], 15)
        self.assertEqual(data["sum_squares"], 55)
        self.assertEqual(data["max"], 5)
        self.assertEqual(data["min"], 1)
        self.assertEqual(data["average"], 3.0)
    
    def test_process_numbers_empty(self):
        """Test process endpoint with empty array."""
        payload = {"numbers": []}
        response = requests.post(f"{self.server_url}/process", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["sum"], 0)
        self.assertEqual(data["sum_squares"], 0)
        self.assertEqual(data["max"], 0)
        self.assertEqual(data["min"], 0)
        self.assertEqual(data["average"], 0)
    
    def test_heavy_computation(self):
        """Test heavy computation endpoint."""
        payload = {"numbers": [1, 2, 3]}
        response = requests.post(f"{self.server_url}/heavy", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["sum_squares"], 14)
        self.assertEqual(data["fibonacci_30"], 832040)
        self.assertEqual(data["processed_length"], 3)
    
    def test_invalid_method(self):
        """Test GET request to POST endpoint."""
        response = requests.get(f"{self.server_url}/process")
        self.assertEqual(response.status_code, 405)
    
    def test_invalid_json(self):
        """Test invalid JSON payload."""
        response = requests.post(
            f"{self.server_url}/process",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()