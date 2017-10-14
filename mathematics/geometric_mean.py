# geometric_mean.py
# by James Fulford

def geometric_mean(numbers):
    """
    mathematics.geometric_mean.geometric_mean
    Returns the geometric mean of a list of numbers.
    In other words:
        returns gm such that
            if n is the number of numbers provided
            and prod is the product (*) of all the numbers,
            then
            gm ** n = prod
    """
    product = 1.0
    for entry in numbers:
        product *= entry
    return product ** (1.0 / len(numbers))
