# fit_curve.py
# by James Fulford

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
# https://youtu.be/iEsWFnpbHb4


import numpy as np
import random

class Models():
    @staticmethod
    def sin(x, A, B, C, D):
        # A sin(Bx + C) + D
        return (A * np.sin((B * x) + C)) + D

    @staticmethod
    def line(x, M, B):
        # Mx + B
        return (M * x) + B

    @staticmethod
    def exp(x, P, k):
        # Pe^kt
        return P * np.exp(x * k)

    @staticmethod
    def polynomial(degree):
        # returns a model of a polynomial of given degree.
        def poly_model(x, *args):
            sums = 0
            for i in range(degree + 1):
                sums += args[i] * (x ** i)
            return sums
        return poly_model

    @staticmethod
    def logistic(x, K, C, r):
        try:
            return K / (1 + (C * np.exp(-r * x)))
        except:
            pass

    @staticmethod
    def get_model(x_data, y_data):
        # goes through and tries many different models
        # does not try polynomial models, as increasing n always increase accuracy.
        # returns model and parameters to use.
        from scipy.optimize import curve_fit
        r_sqr = {}
        for model in [Models.logistic, Models.line, Models.sin, Models.exp]:
            try:
                params, vari = curve_fit(model, x_data, y_data)
                predictions = map(lambda x: model(x, *params), x_data)
                r_sqr[model.__name__] = {
                    "r2": Models.r_squared(x_data, y_data, predictions),
                    "params": params,
                    "model": model,
                    "vari": vari
                }
            except RuntimeError:
                pass  # didn't find it fast enough.
        max_model = {"r2": 0}
        assert len(r_sqr.keys()) > 0
        for key in r_sqr.keys():
            entry = r_sqr[key]
            if max_model["r2"] < entry["r2"]:
                max_model = entry
                max_model["base_model"] = key
        return max_model

    @staticmethod
    def r_squared(x_data, y_data, predictions):
        assert len(x_data) is len(y_data) and len(y_data) is len(predictions)
        residuals = []
        deviations = []
        y_mean = sum(y_data) / float(len(y_data))
        for i in range(len(x_data)):
            residuals.append(y_data[i] - predictions[i])
            deviations.append(y_data[i] - y_mean)
        residuals = sum(map(lambda x: x ** 2, residuals))
        deviations = sum(map(lambda x: x ** 2, deviations))
        return 1 - (residuals / float(deviations))
