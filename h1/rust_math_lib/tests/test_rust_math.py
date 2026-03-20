import lab9_rust_math_lib

def test_sum_squares():
    result = lab9_rust_math_lib.sum_squares([1, 2, 3, 4, 5])
    assert result == 55

def test_factorial():
    assert lab9_rust_math_lib.factorial(5) == 120

def test_quick_sort():
    result = lab9_rust_math_lib.quick_sort([3, 1, 4, 1, 5, 9, 2])
    assert result == [1, 1, 2, 3, 4, 5, 9]

def test_fibonacci():
    assert lab9_rust_math_lib.fibonacci(10) == 55

def test_math_operations():
    ops = lab9_rust_math_lib.MathOperations(5.0)
    assert ops.square() == 25.0
    assert ops.cube() == 125.0
    ops.value = 3.0
    assert ops.square() == 9.0