# _basic.py
# by James Fulford
# __init__ imports all methods in here automatically
# put in separate file because of self-referencing problems:
#       advanced, popultion, and sample have to import a lot
#       of functions from here. Putting them in __init__
#       would either force a lot of "from __init__ import <>"
#       or would cause self-reference problems.


def count(dataset):
    return len(dataset)
    # for readability;


def summation(dataset):
    enlisted = dataset
    if type(enlisted) is dict:
        enlisted = list(enlisted.values())
    if type(enlisted) is not list:
        raise TypeError
    # return reduce(lambda x, y: x + y, enlisted)
    return sum(enlisted)


def mean(dataset, datatype=float):
    """Returns the mean of the given list of numbers
    as a float (default)"""
    return datatype(float(sum(dataset)) / count(dataset))


def frequency(dataset, acs=lambda x: x):
    """Returns a dictionary with a count of how often
        each entry in the dataset shows up
    as each item is accessed by acs (default: identity"""
    def increment(diction, key):
        if key in diction:
            diction[key] += 1
        else:
            diction[key] = 1
        return diction

    count = {}
    for item in dataset:
        try:
            increment(count, acs(item))
        except TypeError:
            if type(acs(item)) is list:
                increment(count, str(frequency(acs(item))))
            else:
                print "_basic.py line 51 reached"
    return count




def mode(dataset, acs=lambda x: x, smallest=False):
    """Returns list of most frequent entries in dataset
    after being accessed by acs (default: str)
    If smallest is True, returns the minimum value of frequent entries.
    """
    high_score = 0
    finalists = []

    freq = frequency(dataset, acs=acs)
    for key in freq.keys():
        if freq[key] > high_score:
            finalists = [key]
            high_score = freq[key]
            continue
        if freq[key] is high_score:
            finalists.append(key)
            continue
    if smallest:
        return minimum(finalists)
    return sorted(finalists)


def maximum(dataset):
    """Returns greatest value in dataset"""
    return sorted(dataset)[-1]


def minimum(dataset):
    """Returns least value in dataset"""
    return sorted(dataset)[0]


def median(dataset):
    ds = sorted(dataset)
    index = int(len(ds) / 2.0 + .5) - 1
    # round up is the +.5, make it 0 indexed is the -1
    if len(ds) % 2 is 0:
        result = [ds[index], ds[index + 1]]
        if result[0] is not result[1]:
            return result
    return [ds[index]]


def datarange(dataset):
    """Returns the range (max - min) of the dataset"""
    return maximum(dataset) - minimum(dataset)


def variance(dataset):
    """ Returns variance for sample data.
    Why divide by n-1? : https://www.youtube.com/watch?v=9ONRMymR2Eg
    """
    x_bar = mean(dataset)
    differences = map(lambda x: x - x_bar, dataset)
    squares = map(lambda x: x * x, differences)
    return float(summation(squares)) / ((count(dataset) - 1))


def standard_deviation(dataset):
    """ Returns standard deviation for sample data """
    return variance(dataset) ** .5


def confidence_deviation(dataset, conf=.95, pop_stdev=None):
    import scipy.stats as st
    conf_coeff = st.norm.ppf(1 - (1 - conf) / 2)
    if pop_stdev:
        deviation = pop_stdev / (count(dataset) ** .5)
    else:
        deviation = standard_deviation(dataset) / (count(dataset) ** .5)
    deviation = conf_coeff * deviation
    return deviation


def confidence_interval(dataset, conf=.95, pop_stdev=None):
    if pop_stdev:
        deviation = confidence_deviation(dataset, conf=conf, pop_stdev=pop_stdev)
    else:
        assert count(dataset) >= 30  # provide population standard deviation!
        deviation = confidence_deviation(dataset, conf=conf)
    return (mean(dataset) - deviation, mean(dataset) + deviation)


def proportion_confidence_interval(dataset, conf=.95):
    """
    If n unspecified, assumed n is count(dataset)
    """
    import scipy.stats as st
    phat = mean(dataset)

    how_many = count(dataset)

    coeff = phat * (1 - phat) / float(how_many)
    coeff = coeff ** .5
    coeff *= st.norm.ppf((conf / 2))
    return (phat - coeff, phat + coeff)


def p_variance(dataset):
    """ Returns variance for population data """
    x_bar = mean(dataset)
    differences = map(lambda x: x - x_bar, dataset)
    squares = map(lambda x: x * x, differences)
    return mean(squares)


def p_standard_deviation(dataset):
    """ Returns standard deviation for population data """
    return p_variance(dataset) ** .5


def one_var_stats(datapoints, decl):
    """
    decl:
        "nominal" : "equality" is defined
        "ordinal" : "less than" is defined
        "interval": "difference" is defined
    """
    stats = []
    nominal = [mode, count]
    ordinal = [maximum, minimum, median]
    interval = [mean, standard_deviation, variance, datarange, confidence_interval]

    stats.extend(nominal)
    if decl.__contains__("ordinal"):
        stats.extend(ordinal)
    if decl.__contains__("interval"):
        stats.extend(ordinal)
        stats.extend(interval)

    reports = {}
    for stat in stats:
        reports[stat.__name__] = stat(datapoints)
    return reports

def pearson_r(x_data, y_data):
    """
    Returns r-value based on linear model
    for x and y data provided
    """
    assert count(x_data) == count(y_data)
    x_mean = mean(x_data)
    y_mean = mean(y_data)
    X = map(lambda x: x - x_mean, x_data)
    Y = map(lambda y: y - y_mean, y_data)
    numerator = 0
    for i in range(count(X)):
        numerator += X[i] * Y[i]

    denominator = 1
    denominator *= sum(map(lambda x: x ** 2, X)) ** .5
    denominator *= sum(map(lambda x: x ** 2, Y)) ** .5
    try:
        return numerator / denominator
    except ZeroDivisionError:
        # print "\t"*3 + "Pearson's R returns None:"
        # print "\t"*4 + str(x_data)
        # print "\t"*4 + str(y_data)
        return None  # can't calculate pearson's r if all values are the same!
        # there's no variation to correlate with!


def two_var_stats(x_data, x_decl, y_data, y_decl):
    x_stat_type = x_decl["stat_type"]
    y_stat_type = y_decl["stat_type"]
    X = x_data
    Y = y_data
    cor_stat_types = ["ordinal", "interval"]
    if x_stat_type is "nominal" and y_stat_type is "nominal":
        # chi square relationship test
        pass
    elif x_stat_type in cor_stat_types and y_stat_type in cor_stat_types:
        if x_stat_type is "ordinal":
            # map X to integers
            pass
        if y_stat_type is "ordinal":
            # map Y to integers
            pass


def percentile(ds, perc):
    percentile = perc
    if perc >= 1:
        percentile = float(perc) / 100

    listed = sorted(ds)
    index = ((count(ds) - 1) * float(percentile))
    if abs(index - int(index)) < .0001:
        return listed[int(index)]
    upper = int(round(index + .5))
    uppershare = 1 - float(upper - index)
    lower = int(round(index - .5))
    lowershare = 1 - float(index - lower)
    return (listed[upper] * uppershare) + (listed[lower] * lowershare)


def five_point_summary(ds):
    return (minimum(ds), percentile(ds, 25), percentile(ds, 50), percentile(ds, 75), maximum(ds))
