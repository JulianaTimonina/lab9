package main

import (
	"bytes"
	"log"
	"strings"
	"testing"
	"time" // Добавляем импорт time
)

// TestProcessNumbersCalculation - тест вычисления суммы квадратов
func TestProcessNumbersCalculation(t *testing.T) {
	// Сохраняем оригинальный вывод логов
	originalOutput := log.Writer()
	defer log.SetOutput(originalOutput)

	// Создаем буфер для захвата логов
	var buf bytes.Buffer
	log.SetOutput(&buf)

	tests := []struct {
		name     string
		numbers  []int
		expected string // ожидаемая часть сообщения в логе
	}{
		{
			name:     "Positive numbers",
			numbers:  []int{1, 2, 3, 4, 5},
			expected: "Сумма квадратов чисел [1 2 3 4 5] = 55",
		},
		{
			name:     "Negative numbers",
			numbers:  []int{-1, -2, -3},
			expected: "Сумма квадратов чисел [-1 -2 -3] = 14",
		},
		{
			name:     "Mixed numbers",
			numbers:  []int{-2, 3, -4},
			expected: "Сумма квадратов чисел [-2 3 -4] = 29",
		},
		{
			name:     "Single number",
			numbers:  []int{10},
			expected: "Сумма квадратов чисел [10] = 100",
		},
		{
			name:     "Zeros",
			numbers:  []int{0, 0, 0},
			expected: "Сумма квадратов чисел [0 0 0] = 0",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Очищаем буфер перед каждым тестом
			buf.Reset()

			// Вызываем тестируемую функцию
			processNumbers(tt.numbers)

			// Получаем записанный лог
			logOutput := buf.String()

			// Проверяем, что лог содержит ожидаемое сообщение
			if !strings.Contains(logOutput, tt.expected) {
				t.Errorf("Ожидалось сообщение содержащее '%s', получено '%s'", tt.expected, logOutput)
			}
		})
	}
}

// TestProcessNumbersAsyncBehavior - тест асинхронного поведения
func TestProcessNumbersAsyncBehavior(t *testing.T) {
	// Сохраняем оригинальный вывод логов
	originalOutput := log.Writer()
	defer log.SetOutput(originalOutput)

	// Создаем буфер для захвата логов
	var buf bytes.Buffer
	log.SetOutput(&buf)

	// Запускаем функцию и замеряем время
	done := make(chan bool)
	start := time.Now()

	go func() {
		processNumbers([]int{1, 2, 3})
		close(done)
	}()

	select {
	case <-done:
		elapsed := time.Since(start)
		// Проверяем, что функция отработала примерно 2 секунды
		if elapsed < 2*time.Second {
			t.Errorf("Функция завершилась слишком быстро: %v, ожидалось ~2 секунды", elapsed)
		}
		if elapsed > 3*time.Second {
			t.Errorf("Функция выполнялась слишком долго: %v, ожидалось ~2 секунды", elapsed)
		}
	case <-time.After(3 * time.Second):
		t.Error("Функция не завершилась в течение 3 секунд")
	}
}