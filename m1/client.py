import requests
import json

def send_numbers(numbers):
    url = "http://localhost:8080/process"
    
    payload = {
        "numbers": numbers
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 202:
            print("Ответ от сервера:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"Ошибка: статус код {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Ошибка подключения: убедитесь, что сервер запущен на порту 8080")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    # Тестовые данные
    test_numbers = [1, 2, 3, 4, 5]
    
    print(f"Отправляем числа: {test_numbers}")
    send_numbers(test_numbers)
 