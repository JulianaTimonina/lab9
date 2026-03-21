package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

type ComputeRequest struct {
	Numbers []int `json:"numbers"`
}

type ComputeResponse struct {
	SumSquares int     `json:"sum_squares"`
	Sum        int     `json:"sum"`
	Max        int     `json:"max"`
	Min        int     `json:"min"`
	Average    float64 `json:"average"`
}

type HeavyResponse struct {
	SumSquares      int `json:"sum_squares"`
	Fibonacci30     int `json:"fibonacci_30"`
	ProcessedLength int `json:"processed_length"`
}

func sumSquares(numbers []int) int {
	sum := 0
	for _, n := range numbers {
		sum += n * n
	}
	return sum
}

func fibonacci(n int) int {
	if n <= 1 {
		return n
	}
	a, b := 0, 1
	for i := 1; i < n; i++ {
		a, b = b, a+b
	}
	return b
}

func processNumbersHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req ComputeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if len(req.Numbers) == 0 {
		resp := ComputeResponse{
			SumSquares: 0,
			Sum:        0,
			Max:        0,
			Min:        0,
			Average:    0,
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(resp)
		return
	}

	sum := 0
	max := req.Numbers[0]
	min := req.Numbers[0]
	for _, n := range req.Numbers {
		sum += n
		if n > max {
			max = n
		}
		if n < min {
			min = n
		}
	}
	average := float64(sum) / float64(len(req.Numbers))

	resp := ComputeResponse{
		SumSquares: sumSquares(req.Numbers),
		Sum:        sum,
		Max:        max,
		Min:        min,
		Average:    average,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func heavyComputationHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req ComputeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	resp := HeavyResponse{
		SumSquares:      sumSquares(req.Numbers),
		Fibonacci30:     fibonacci(30),
		ProcessedLength: len(req.Numbers),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

func main() {
	http.HandleFunc("/process", processNumbersHandler)
	http.HandleFunc("/heavy", heavyComputationHandler)
	http.HandleFunc("/health", healthCheckHandler)

	port := 8080
	fmt.Printf("Go HTTP server starting on http://localhost:%d\n", port)
	fmt.Println("Endpoints:")
	fmt.Println("  POST /process - Process numbers")
	fmt.Println("  POST /heavy   - Heavy computation")
	fmt.Println("  GET  /health  - Health check")
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", port), nil))
}