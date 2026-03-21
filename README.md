# Лабораторная работа №9
##Вариант 9

### Задания

| Задание | Описание |
|---------|----------|
| М1 | 2.Добавить горутину для фоновой обработки запросов |
| М2 | 4.Передать данные из Python в Go через JSON (stdin/stdout) |
| М3 | 9.Сравнить скорость выполнения Rust-функции и аналогичной на Python |
| В1 | 3.Настроить сборку Rust-модуля в CI/CD и публикацию на PyPI |
| В2 | 5.Профилировать и сравнить производительность трёх решений: Python, Python+Rust, Python+Go (как внешний сервис) |

---

### Структура репозитория

```
lab9/
├── README.md
├── PROMPT_LOG.md
├── PROMPT_LOG.md
├── .gitignore
├── .github/workflows
│       └── ci-cd.yml
├── m1/
│   ├── client.py
│   ├── go.mod
│   ├── main.go
│   ├── main_test.go
│   └── process_numbers_test.go
├── m2/
│   ├── calculator.go
│   ├── main.py
│   └── test_integration.py
├── m3/
│   ├── main.py
│   ├── test_speed.py
│   └── rust_math/
│       ├── Cargo.toml
│       └── src/lib.rs
├── h1/rusth_math_lib
│       ├── Cargo.toml
│       ├── pyproject.toml
│       └── src/lib.rs
│       └── tests/
│           └── test_rust_math.py
└── h2/
    ├── go_service/
    │   ├── go.mod
    │   ├── main.go
    │   └── test_go_service.py
    ├── python_only/
    │   ├── calculator.py
    │   └── test_calculator.py
    ├── rust_lib/
    │   ├── Cargo.toml
    │   ├── test_fastmath.py
    │   └── src/lib.rs
    ├── benchmark.py
    ├── requirements.txt
    └── test_all.py
```

## Запуск тестов

### М1
Добавить горутину для фоновой обработки запросов

```bash
# Запуск сервера
go run main.go

# В другом терминале запуск клиента
python client.py

# Запуск тестов
go test -v
```

#### М2
Передать данные из Python в Go через JSON (stdin/stdout)

```bash
# Компиляция
go build -o calculator calculator.go

# Запуск клиента
python main.py

# Запуск тестов
python test_integration.py -v
```

#### М3
Сравнить скорость выполнения Rust-функции и аналогичной на Python

```bash
# Вариант 1: Сборка с maturin (рекомендуется)
pip install maturin
cd rust_math
maturin develop
cd ..

# Вариант 2: Сборка вручную
cd rust_math
cargo build --release
cd ..
pip install -e .

# Запуск сравнения производительности
python main.py

# запуск тестов
python test_speed.py -v
```

#### В1
Настроить сборку Rust-модуля в CI/CD и публикацию на PyPI

```bash
# Библиотека опубликована на PyPI

# Установите из PyPI
pip install lab9-rust-math-lib

# Локальная сборка и тестирование
# Создайте виртуальное окружение
python -m venv .venv
# Активируйте
.venv\Scripts\activate

# Установите maturin
pip install maturin pytest

# Соберите и установите
maturin develop

# Запустите тесты
pytest tests/ -v
```

#### В2
Профилировать и сравнить производительность трёх решений: Python, Python+Rust, 
Python+Go (как внешний сервис). 

```bash
# Установка зависимостей
pip install -r requirements.txt

# Сборка Rust библиотеки
cd rust_lib
maturin develop --release
cd ..

# Сравнение производительности
python benchmark.py

# Запуск тестов
python test_all.py
```

### Требования

| Инструмент | Версия | Примечание |
|-----------|--------|------------|
| Go | 1.21+ | |
| Rust + Cargo | 1.70+ | |
| Python | 3.13 | |
| maturin | любая | `python -m pip install maturin` |
| pytest | любая | `python -m pip install pytest` |
