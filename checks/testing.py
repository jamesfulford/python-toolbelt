# testing.py
from checks import check


square_tests = [
    {"args": [1], "expected": 2},
    {"args": 2, "expected": 5, "should_pass": True},
    {"args": [3], "expected": 11, "should_pass": False},
    {"args": [4], "kwargs": {"a": 0}, "expected": 16, "should_pass": True}
]


# function to test
def square(x, a=0):
    return (x ** 2) + a


@check(square_tests, a=1)
def test_square(*args, **kwargs):
    return square(*args, **kwargs)
