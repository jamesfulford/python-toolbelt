# testing_checks.py
from checks import check_json


# function to test
def square(x, a=0):
    return (x ** 2) + a


@check_json(open("square_tests.json"))
def test_square(*args, **kwargs):
    return square(*args, **kwargs)
