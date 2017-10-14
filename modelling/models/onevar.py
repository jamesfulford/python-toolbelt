# models.py
# by James Fulford

import numpy as np
from model import SingleModel

class sin(SingleModel):
    """
    A sin(Bx + C) + D
    """
    @staticmethod
    def __call__(x, A, B, C, D):
        return (A * np.sin((B * x) + C)) + D

class line(SingleModel):
    """
    mx + b
    """
    @staticmethod
    def __call__(x, m, b):
        return (m * x) + b

class exp(SingleModel):
    """
    Pe^kt
    """
    @staticmethod
    def __call__(x, P, k):
        return P * np.exp(x * k)

class logistic(SingleModel):
    """
    K: carrying capacity
    C and r have something to do with growth
    Be advised of dividing by 0 errors
    """
    @staticmethod
    def __call__(x, K, C, r):
        return K / (1 + (C * np.exp(-r * x)))
