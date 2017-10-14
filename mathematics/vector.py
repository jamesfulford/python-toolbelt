# vector.py
# Use this to do math stuffs!
# by James Fulford
# Began: 6/8/2016
# Stopped Developing:

import math


def polarToCartesian(argument_radians, magnitude):
    """
    mathematics.vector.polarToCartesian
    Returns a 2-tuple (x, y) representation of given arg and mag.
    """
    x = math.cos(argument_radians) * magnitude
    y = math.sin(argument_radians) * magnitude
    return (x, y)


def addTuples(tuple1, tuple2):
    """
    mathematics.vector.addTuples
    Adds each entry of two tuples to one another. Returns a tuple.
    """
    result = []
    for i in range(0, max(len(tuple1), len(tuple2))):
        try:
            result.append(tuple1[i] + tuple2[i])
        except:
            try:
                result.append(tuple1[i])
            except:
                try:
                    result.append(tuple2[i])
                except:
                    result.append(0)  # this shouldn't run,
                    # because the range shouldn't let it.
    return tuple(result)
