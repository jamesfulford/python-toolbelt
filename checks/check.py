# check.py
# by James Fulford
# Provides cool decorators
# to assist in unittesting
# with the nosetests command


from functools import wraps
import json


def is_equal(a, b):
    return a == b


def is_in(a, b):
    return a in b


def is_identical(a, b):
    return a is b


def each_in(a, b):
    return reduce(lambda x, y: x and y, map(lambda ai: ai in b, a))


def unordered_equal(a, b):
    return set(a) == set(b)


def _silence():
    # purposefully does nothing
    pass

# todo: make set_up and tear_down work usefully? Pass state object???
def check(tests, post_transform=lambda x: x, comparer=is_equal,
          set_up=_silence, tear_down=_silence, **kwargs):
    """Tests list of cases, represented as dictionaries
        "should_pass": True
            [True, False]
        "args": ("",)
            single non-list arguments need not be in a list/tuple.
        "kwargs": {}
            can set default kwarg values using this functions kwargs
        "expected": required


    post_transform will transform output of decorated function before comparing
    comparer is the function which compares output and expectations
        and returns False if it fails the test, true otherwise.

    set_up will run before tests
    tear_down will run after tests

    Uses test generators:
    https://nose.readthedocs.io/en/latest/writing_tests.html#test-generators

    Got wrapping help off of Stack Overflow from Zero Piraeus's answer:
    https://stackoverflow.com/questions/13611658/repeated-single-or-multiple-tests-with-nose
    """

    def wrap(fn):
        """
        Will be called with the test function as a parm.
        """
        @wraps(fn)
        def wrapper():
            """
            nosetests will treat this as a test generator and
            will consider each item in tests as a separate test.
            """

            #
            # Set up before all tests
            #
            set_up()

            for test in tests:
                #
                # Parse test dictionaries
                #
                expected = test["expected"]
                args = test.get("args", ("",))
                key_words = {}
                for key in kwargs.keys():
                    key_words[key] = kwargs[key]
                for key, value in test.get("kwargs", {}).items():
                    key_words[key] = value
                should_pass = test.get("should_pass", True)
                assert should_pass in [True, False], "Needs to be boolean"

                #
                # Find output of function
                #

                # handle single argument case
                if type(args) not in [list, tuple]:
                    args = (args,)

                actual = fn(*args, **key_words)
                actual = post_transform(actual)

                r = comparer(actual, expected)
                if not should_pass:
                    r = not r

                #
                # Making error message
                #

                msg = fn.__name__
                try:  # Try to convert args and kwargs to strings
                    msg += "({}".format(", ".join(map(str, args)))
                    if key_words:
                        msg += ", **{}".format(key_words)
                    msg += ")"
                except Exception:
                    pass
                msg += "\nShould pass: {}\n".format(should_pass)

                try:  # Try to convert actual and expected to strings
                    msg += "\n[  actual  ] {}\n[ expected ] {}\n" \
                        .format(actual, expected)
                except Exception:
                    pass

                #
                # Return generated function
                #
                def do():
                    assert r, msg
                yield do

            #
            # Tear Down after all tests
            #
            tear_down()

        return wrapper
    return wrap


def check_json(file, **kwargs):
    return check(json.load(file), **kwargs)
