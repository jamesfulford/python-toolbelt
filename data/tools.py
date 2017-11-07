
# tools.py
import logging
logger = logging.getLogger(__name__)


#
# These constants define what types
# invoke what type of behavior in all
# recursive functionality in this package
#

# list functionalities
ITERABLES = (
    list,
    tuple,
    # numpy.Array?
)

# dictionary functionalities
DICTIONARIES = (
    dict,
    # collections.OrderedDict?
)

# string functionalities
STRINGS = (
    str,
    unicode,
)


def partition(fn, ls):
    """
    Calls fn on each item in ls
        returns dictionary keyed on outputs of fn
        values being lists of items with that output

    >>> partition(lambda x: x ** 2, [1, 2, 3, -2])
    {1: [1], 4: [2, -2], 9: [3]}

    >>> partition(bool, [1, 0, [], "Hello"])
    {True: [1, "Hello"], False: [0, []]}
    """
    parting = {}
    for item in ls:
        r = fn(item)
        try:
            parting[r].append(item)
        except KeyError:
            parting[r] = [item]
    return parting


def resolve_keypath(keypath, split="/"):
    """
    Converts keypath into a list of keys to pass through.
    If keypath is a string, makes list by splitting on split

    >>> resolve_keypath(["a", "b"])
    ["a", "b"]

    >>> resolve_keypath("a/b")
    ["a", "b"]

    >>> resolve_keypath("a_b", split="_")
    ["a", "b"]

    """
    if isinstance(keypath, STRINGS):
        if split:
            keypath = keypath.split(split)
        else:
            keypath = [keypath]
    return keypath


def flatten_list(list_of_lists, depth=True):
    """Given a list of lists, unpacks all the items
    and puts it in one list.

    depth specifies how many layers deep we should flatten.
        by default flattens all layers

    >>> flatten_list([[1, [2], [3, 4]], [[5, [6, 7], [8]]]])
    [1, 2, 3, 4, 5, 6, 7, 8]

    >>> flatten_list([[1, [2], [3, 4]], [[5, [6, 7], [8]]]], depth=2)
    [1, 2, 3, 4, 5, [6, 7], [8]]
    """
    result = []
    for item in list_of_lists:
        if isinstance(item, ITERABLES):
            if type(depth) is int and depth - 1 >= 0:
                # flatten this level
                result.extend(flatten_list(item, depth=depth - 1))
            elif depth:
                # flatten all the way down
                result.extend(flatten_list(item))
            else:
                # preserve
                result.append(item)
        else:
            result.append(item)
    return result


def pass_through(value, mapping, warn=False, **kwargs):
    """Tries to map value through mapping. If fails, returns input.
    Mapping can be a function or a dictionary.

    If function, key words are passed down to the function.
        Exceptions are caught and printed, returns value

    If dictionary, tries to get new value by inputting the value.
        If value is not hashable (list, set, etc.), prints and returns value

    >>> pass_through(2, lambda x: x ** 2)
    4

    >>> pass_through("color", {"color": "BLUE"})
    "BLUE"

    >>> pass_through("color", {"id": 42})
    "color"

    >>> pass_through(["unhashable"], {"id": 42})
    ["unhashable"]  # also prints error to stdout

    >>> pass_through(0, lambda x: 1/x)
    0  # prints error to stdout

    """

    # Lists cannot pass_through. Instead, we pass through all items.
    # If a staggered, unflattened list of lists,
    #   will pass all entries and lower entries through
    if isinstance(value, ITERABLES):
        return map(lambda v: pass_through(v, mapping, warn=False, **kwargs),
                   value)

    if isinstance(value, DICTIONARIES):
        try:
            return mapping.get(value, value)
        except TypeError:
            msg = "pass_through: TypeError (unhashable type?)" \
                ": cannot get {} from {}".format(value, mapping)
            logger.debug(msg)
            print msg
            # will return value later
        except KeyError:
            # this is expected behavior
            pass  # will return value later
    else:
        try:
            return mapping(value, **kwargs)
        except Exception as e:  # calling the function failed
            msg = "pass_through: {}({}) failed\n".format(
                value, mapping.__name__) + str(e)
            logger.debug(msg)
            print msg

    # Mapping failed - return input
    return value


def check(data, form, *context):
    """
    Checks data complies with tests specified in form.
    If test fails, prints value returned and returns False
        continues to evaluate tests
    Is part of validation.
    """

    if isinstance(form, DICTIONARIES):
        # delegate to all key-value pairs
        results = []
        for key, value in form.items():
            result = check(data[key], value, *context)
            results.append(result)
            if not result:
                break
        return reduce(lambda p, q: bool(p) and bool(q), results)
    elif isinstance(form, ITERABLES):
        # delegate to all items
        results = []
        for item in data:  # data should be a list
            result = check(item, form[0], *context)
            results.append(result)
            if not result:
                break
        return reduce(lambda p, q: bool(p) and bool(q), results)
    else:
        # Leaf of form
        try:
            # Call the validator on this piece of data
            output = form(data, *context)
        except Exception as e:
            output = str(e)

        if output is not True:
            print "{}({}) failed (output: {})" \
                .format(form.__name__, data, output)
            return False
        return True
