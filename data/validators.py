# validators.py
# by James Fulford

#
# Probably the most moral Python I've ever written
# -James Fulford
#

from accessors import access
from tools import ITERABLES

#
# CONTEXT DEFINITIONS
#
# No context: validating just the value present
#       (useful for datatype checks)
#
# First context: validating against other fields in entry
#       (useful for one field less than another)
#
# Second context: validating against other entries in list
#       (useful for graph references and uniqueness)
#
# Third context: validating against entries in named lists (dictionary)
#       (useful for foreign references)
#


#
# TODO: make these rules representable with __repr__
# Decorator? Needs to know all args, kwargs
# __str__ = __repr__  for error messages
#


def should(*args):
    """
    Aggregates multiple tests in an 'AND' fashion (all must pass)

    If a test is a list, at least 1 must pass (OR)
        If a subtest is a list, all must pass (AND)
            If a subsubtest is a list, at least 1 must pass (OR)
    (Continues to alternate.)

    Stops list execution if
        'AND' lists: one fails
        'OR' lists: one succeeds

    >>> should(
        # ALL
        be_a(dict),  # YEP
        [   # EITHER
            [   # ALL
                have("death"),  # YEP
                lambda d: d["death"] is True  # NOPE - "AND" FAILS
            ],
            have("liberty", be_an(int)),  # YEP - OR SUCCEEDS
        ]  # YEP - AND SUCCEEDS
    )({"liberty": 22, "death": False})
    True
    """
    return _parse_tests(args, top_is_and=True)


def at_least(*args):
    """
    Aggregates multiple tests in an 'OR' fashion (1 must pass)

    If a test is a list, all must pass (AND)
        If a subtest is a list, at least 1 must pass (OR)
            If a subsubtest is a list, all must pass (AND)
    (Continues to alternate.)

    Stops list execution if
        'AND' lists: one fails
        'OR' lists: one succeeds

    >>> case(
        # EITHER
        be_a(dict),  # YEP - STOPS EXECUTION
        [   # ALL
            [   # EITHER
                have("death"),
                lambda d: d["death"] is True
            ],
            have("liberty", be_an(int)),
        ]
    )({"liberty": 22, "death": False})
    True
    """
    return _parse_tests(args, top_is_and=False)


def case(*args):
    #
    # TODO: Make it like at_least, but on an XOR basis
    # (ONE AND ONLY ONE SUCCEEDS)
    #
    pass


def _parse_tests(args, top_is_and=True):
    #
    # TODO: Be able to specify number of successes needed
    # i.e. need at least 2 tests to pass in order for this to pass
    #

    def check_that(data, *context):

        def check_and(arg, depth=0):
            if isinstance(arg, ITERABLES):
                # print ("    " * depth) + "AND({})".format(arg)
                for a in arg:
                    #
                    # If one test fails,
                    # prematurely return False
                    #
                    if not check_or(a, depth=depth + 1):
                        # lower level alternation
                        return False
                return True
            else:
                return arg(data)

        def check_or(arg, depth=0):
            if isinstance(arg, ITERABLES):
                # print ("    " * depth) + "OR({})".format(arg)
                for a in arg:
                    #
                    # If one test succeeds,
                    # prematurely return True
                    #
                    if check_and(a, depth=depth + 1):
                        # lower level alternation
                        return True
                return False
            else:
                return arg(data)

        if top_is_and:
            return check_and(args, depth=0)
        else:
            return check_or(args, depth=0)

    return check_that


#
# No context validators
#


def be(*goods):
    def is_good(data, *context):
        return data in goods
    return is_good


def be_in(good_list, *context):
    return be(*good_list)


def be_a(*good_types):
    def good_type_or_not(data, *context):
        return isinstance(data, tuple(good_types))
    return good_type_or_not


be_an = be_a  # makes my english feel better


def be_truthful(data, *context):
    return bool(data)


def be_good(good_test):
    def is_test_good(data, *context):
        return good_test(data, *context)
    return is_test_good


def have(key, *tests):
    """
    Returns if key successfully accessed from data.
    Will call should with args, passing in accessed value.

    >>> have("liberty")({"liberty": 32})
    True

    >>> have("liberty", be_an(int))({"liberty": 32})
    True
    """
    tests = should(*tests)

    def try_access(data, *context):
        try:
            result = access(key)(data)
        except Exception:
            return False
        else:  # make sure validation errors not caught
            return tests(result, *context)

    return try_access


#
# First Contextual Validators
#

#
# TODO: Add first context validators
#


#
# Second Contextual Validators
#

#
# TODO: convert these to second context validators
#


def _reference(key, min_finds, max_finds=None, flatten=True):
    """
    Returns refer, which accesses key from each item
        in second context's list

    If data is found less than min_finds times
        or more than max_finds times (if specified)
        returns False.
    Otherwise, returns True.

    If accessed value is a list, looks for datavalue in list
        (List is flattened by default)
    """
    def refer(data, me, ls, *args):
        finds = 0
        for item in ls:
            acc = access(key, flatten=flatten)(item)
            if isinstance(acc, ITERABLES):
                result = data in acc
            else:
                result = data == acc
            if result:
                finds += 1
                if max_finds and finds > max_finds:
                    return False
        return finds >= min_finds
    return refer


def be_unique(key):
    """
    Returns True if value shows up only once in the list
        after accessing key from each item in first context list.

    Returns False for ALL entries with conflicts.
    """
    return _reference(key, 1, 1)


def point_to(key):
    """
    Returns True if value shows up at least once in the list
        after accessing key from each item in first context list.

    Else, False.
    """
    return _reference(key, 1)


#
# Third Context Validators
#

#
# TODO: Specify test(s) to run on foreign referred item
#
def foreign(nexi_name, key, *tests):
    """
    Returns function which checks uniqueness on third context
    """
    # test = should(*tests) if tests else be_unique
    def foreign_reference(data, me, ls, nexi, *contexts):
        return be_unique(key)(data, me, nexi[nexi_name], nexi, *contexts)
    return foreign_reference


if __name__ == "__main__":
    print should(
        # ALL
        be_a(dict),
        [   # EITHER
            [   # ALL
                have("death"),
                lambda d: d["death"] is True
            ],
            have("liberty", be_an(int)),
        ]
    )({"liberty": 22, "death": False})
