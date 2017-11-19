# statistics_and_tests.py
# by James Fulford

from _basic import *


def chi_square_stat(observed, expected):
    """
    Returns confidence interval that categories of x and categories of y
    have a relationship by means of frequency.
    """
    diff = []
    for i in range(len(observed)):
        cal = float(observed[i]-expected[i]) ** 2
        diff.append(cal / expected[i])
    return sum(diff)


def ds_likely_same_means(ds1, ds2, d=0, two_sided=False):
    mean1, stdev1, n1 = mean(ds1), standard_deviation(ds1), count(ds1)
    mean2, stdev2, n2 = mean(ds2), standard_deviation(ds2), count(ds2)

    prob = likely_same_means(mean1, stdev1, n1, mean2, stdev2, n2, d=d, two_sided=two_sided)

    from scipy import stats
    # print prob, stats.ttest_ind(ds1, ds2)[1]
    return prob


def likely_same_means(mean1, stdev1, n1, mean2, stdev2, n2, d=0, two_sided=False):
    s1 = float(stdev1**2 / n1)
    s2 = float(stdev2**2 / n2)
    se = (s1 + s2) ** .5

    df = (s1 ** 2) / float(n1 - 1)
    df += (s2 ** 2) / float(n2 - 1)
    if df < 0.0001:
        df = int(min(n1 - 1, n2 - 1))
    else:
        df = int(round(((s1 + s2) ** 2) / df))

    t = (abs(mean1 - mean2) - d) / se

    from scipy import stats as st
    if two_sided:
        return st.t.cdf(-abs(t), df) * 2
    return st.t.sf(t, df)


# Uses Z or T statistic to calculate likelyhood that sample_center is
def likely_typical_sample_mean(sample_center, pop_center, sample_n, pop_variance=None, sample_variance=None, two_sided=False):
    """
    (observed, population, n, either pop_variance or sample_variance, optional two_sided)
    Returns probability of getting the observed value. (Lower is stronger evidence.)
    Uses t-statistic for small n if pop_variance not known
    Otherwise uses z-statistic
    (approximates pop_variance with sample_variance / sqrt(sample_n))
    """
    stat = float(sample_center - pop_center)
    if pop_variance is not None:
        stat = stat / (pop_variance / (sample_n ** .5))
        use_z_statistic = True
    else:
        assert sample_variance is not None  # you need one of the two!
        stat = stat / (sample_variance / (sample_n ** .5))
        if sample_n > 30:
            use_z_statistic = True
        else:
            use_z_statistic = False

    from scipy import stats as st
    if use_z_statistic is True:
        # return p-value with normal distribution
        prob = st.norm.cdf(-abs(stat))
    else:
        # return p-value with t-distribution
        prob = st.t.cdf(-abs(stat), sample_n - 1)  # ? take out -abs?

    if two_sided:
        prob = prob * 2
    return prob
