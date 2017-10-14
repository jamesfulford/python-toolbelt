# model.py
# by James Fulford

from matplotlib import pyplot as plt


class Model():
    def __init__(self, func):
        self.func = func

        from inspect import getargspec
        self.count_inputs = len(getargspec(func)[0])

    def __call__(self, *values):
        return self.func(*values)  # if func is vectorized, so will this.

    def r_squared(self, inputs, observations):
        assert len(inputs) is len(observations)
        predictions = map(self.func, inputs)
        residuals = []
        deviations = []
        y_mean = sum(observations) / float(len(observations))
        for i in range(len(inputs)):
            residuals.append(observations[i] - predictions[i])
            deviations.append(observations[i] - y_mean)
        residuals = sum(map(lambda x: x ** 2, residuals))
        deviations = sum(map(lambda x: x ** 2, deviations))
        return 1 - (residuals / float(deviations))


class SingleModel(Model):
    def __init__(self, func):
        Model.__init__(self, func)
        assert self.count_inputs == 1

    def plot(self, inputs):
        plt.plot(inputs, map(self.func, inputs))

    @classmethod
    def fit(cls, inputs, observations):
        from scipy.optimize import curve_fit
        func = cls
        if issubclass(cls, SingleModel):
            func = cls.__call__
        params, vari = curve_fit(func, inputs, observations)
        return SingleModel(lambda x: func(x, *params))

