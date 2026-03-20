package main

import (
	"encoding/json"
	"fmt"
	"os"
)

// Input структура для входящих данных
type Input struct {
	Numbers []int `json:"numbers"`
}

// Output структура для результата
type Output struct {
	Sum        int   `json:"sum"`
	SquareSum  int   `json:"square_sum"`
	Processed  []int `json:"processed"`
	Status     string `json:"status"`
}

func main() {
	var input Input
	
	// Читаем JSON из stdin
	decoder := json.NewDecoder(os.Stdin)
	err := decoder.Decode(&input)
	if err != nil {
		// В случае ошибки возвращаем JSON с ошибкой
		output := Output{
			Status: fmt.Sprintf("error: %v", err),
		}
		json.NewEncoder(os.Stdout).Encode(output)
		os.Exit(1)
	}

	// Вычисляем сумму и сумму квадратов
	sum := 0
	squareSum := 0
	processed := make([]int, len(input.Numbers))
	
	for i, n := range input.Numbers {
		sum += n
		square := n * n
		squareSum += square
		processed[i] = square
	}

	// Формируем результат
	output := Output{
		Sum:        sum,
		SquareSum:  squareSum,
		Processed:  processed,
		Status:     "success",
	}

	// Отправляем JSON в stdout
	encoder := json.NewEncoder(os.Stdout)
	encoder.Encode(output)
}