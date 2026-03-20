package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type Request struct {
	Numbers []int `json:"numbers"`
}

type Response struct {
	SumSquares int    `json:"sum_squares"`
	Message    string `json:"message"`
}

func processHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req Request
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	// Проверяем, что numbers не пустой
	if len(req.Numbers) == 0 {
		http.Error(w, "Numbers array cannot be empty", http.StatusBadRequest)
		return
	}

	// Запускаем горутину для фоновой обработки
	go processNumbers(req.Numbers)

	// Немедленно возвращаем ответ
	response := Response{
		SumSquares: 0,
		Message:    "Запрос принят, обработка в фоне",
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusAccepted)
	json.NewEncoder(w).Encode(response)
}

func processNumbers(numbers []int) {
	// Имитируем тяжелую обработку
	time.Sleep(2 * time.Second)

	// Вычисляем сумму квадратов
	sum := 0
	for _, num := range numbers {
		sum += num * num
	}

	// Выводим результат в лог
	log.Printf("Сумма квадратов чисел %v = %d", numbers, sum)
}

func main() {
	http.HandleFunc("/process", processHandler)
	
	log.Println("Сервер запущен на порту 8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("Ошибка запуска сервера:", err)
	}
}
