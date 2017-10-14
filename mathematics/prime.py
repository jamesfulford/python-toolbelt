# fulford_function.py
# by James Fulford

import math


def primes(limit, less_than=False):
    """
    mathematics.prime.primes
    Returns limit-long list of primes of provided length.
    If less_than=True, then returns all prime numbers less than limit.
    """
    primes = [2, 3]

    while(True):
        ind = primes[-1]
        if less_than:
            if ind >= limit:
                break
        else:
            if len(primes) >= limit:
                break
        is_prime = True
        for number in primes:
            if number > int(math.sqrt(ind)):
                break
            if ind % number == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(ind)
        ind += 2
    return primes


def is_prime(num):
    """
    mathematics.prime.is_prime
    Returns whether given number num is prime or not.
    """
    is_prime = True
    for number in primes(int(math.sqrt(num)) + 1, less_than=True):
        if number > int(math.sqrt(num)):
            break
        if num % number == 0:
            is_prime = False
            break
    return is_prime


def fulford_function(exponents):
    """
    mathematics.prime.fulford_function
    Returns unique number for given list of exponents.
    Specifically:
        Returns PROD(p[i] ** exp[i])
        where p[i] is the ith prime
        and exp[i] is the ith number provided as the argument.
        (PROD just means multiply all these numbers together.)

    Mathematically:
        In this documentation, referred to as f.
        On paper, referred to as a fancy capital F. (for Fulford)
        If all arguments provided are positive ints, then result is an integer.
            can be undone by factoring. (Fundamental Theorem of Arithmetic)

        Ideally, if all arguments are ints, then result is positive rational.

        If arguments are rationals, then result is ... working on that...
            sometimes, I call it "root irrational"

        If arguments are real, then answer is positive real

        If arguments are complex, then answer is real, but not 0

    Examples:
        f[2, 1, 1] -> 2**2 * 3**1 * 5**1 = 4 * 3 * 5 = 60
        f[-1, 3] -> 2**-1 * 3**3 = 27/2 = 13.5
        f[0, 0, -1/2] -> root(5)
        f[0, 0, 0] ->

    """
    count = 1
    prime = primes(len(exponents))
    for i in range(0, len(exponents)):
        count *= prime[i] ** exponents[i]
    return count


# def aks_is_prime(num):
    """
    mathematics.prime.aks_is_prime
    Uses AKS test to determine if num is prime.
    See numberphile video.
    """
#     from polynomial import Polynomial as P
#     poly = P([-1, 1]) ** num  # (x - 1) ^ num
#     off_ends = (poly + P([1]) + P([-1]).mult_by_x(num)).coefficients
#     coeffs = map(lambda x: x / float(num), off_ends)
#     non_ints = filter(lambda x: abs(x - int(x)) > .0001, coeffs )
#     return len(non_ints) is 0
