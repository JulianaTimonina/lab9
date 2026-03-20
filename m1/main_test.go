package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

// TestProcessHandlerValidInput - тест корректного ввода
func TestProcessHandlerValidInput(t *testing.T) {
	// Подготавливаем тестовые данные
	reqBody := Request{
		Numbers: []int{1, 2, 3, 4, 5},
	}
	bodyBytes, _ := json.Marshal(reqBody)

	// Создаем HTTP запрос
	req := httptest.NewRequest(http.MethodPost, "/process", bytes.NewReader(bodyBytes))
	req.Header.Set("Content-Type", "application/json")

	// Создаем ResponseRecorder для записи ответа
	w := httptest.NewRecorder()

	// Вызываем обработчик
	processHandler(w, req)

	// Проверяем статус код
	if w.Code != http.StatusAccepted {
		t.Errorf("Ожидался статус %d, получен %d", http.StatusAccepted, w.Code)
	}

	// Проверяем структуру ответа
	var resp Response
	if err := json.NewDecoder(w.Body).Decode(&resp); err != nil {
		t.Fatalf("Не удалось распарсить ответ: %v", err)
	}

	// Проверяем поля ответа
	if resp.SumSquares != 0 {
		t.Errorf("Ожидалось SumSquares = 0, получено %d", resp.SumSquares)
	}

	if resp.Message != "Запрос принят, обработка в фоне" {
		t.Errorf("Ожидалось сообщение 'Запрос принят, обработка в фоне', получено '%s'", resp.Message)
	}
}

// TestProcessHandlerEmptyNumbers - тест пустого массива чисел
func TestProcessHandlerEmptyNumbers(t *testing.T) {
	// Подготавливаем тестовые данные с пустым массивом
	reqBody := Request{
		Numbers: []int{},
	}
	bodyBytes, _ := json.Marshal(reqBody)

	// Создаем HTTP запрос
	req := httptest.NewRequest(http.MethodPost, "/process", bytes.NewReader(bodyBytes))
	req.Header.Set("Content-Type", "application/json")

	// Создаем ResponseRecorder для записи ответа
	w := httptest.NewRecorder()

	// Вызываем обработчик
	processHandler(w, req)

	// Проверяем статус код (должен быть 400 Bad Request)
	if w.Code != http.StatusBadRequest {
		t.Errorf("Ожидался статус %d, получен %d", http.StatusBadRequest, w.Code)
	}

	// Проверяем сообщение об ошибке
	expectedError := "Numbers array cannot be empty\n"
	if w.Body.String() != expectedError {
		t.Errorf("Ожидалось сообщение '%s', получено '%s'", expectedError, w.Body.String())
	}
}