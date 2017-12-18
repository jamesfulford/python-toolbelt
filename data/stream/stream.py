# stream.py

import time
import threading

import worker_types


#
# TODO: Use "from Queue import Queue" instead of Trickle...
# TODO: Add Streams together to make longer Streams
# TODO: Ensure that Streams inside of Streams are OK
#       (see note in Stream.__call__)
#       (also make sure Errors work nicely)
# TODO: Make some generic Workers (databases, api)
# TODO: Make a function that mutates object in any order (parallel_compose)
# TODO: .then: if worker is dict, parallel_compose vals and name w/ keys
#       and if worker is list, parse each item.
#       and if worker is Worker, do what we do now.
#

class Trickle(object):

    def __init__(self, work):
        self.work = work
        self.i = 0
        self.nomore = False

    def __iter__(self):
        return self

    def __getitem__(self, i):
        return self.work[i]

    def __repr__(self):
        return "Tricker({})".format(self.work)

    __str__ = __repr__

    def append(self, item):
        self.work.append(item)

    def extend(self, items):
        self.work.extend(items)

    def next(self):
        try:
            ret = self.work[self.i]
            self.i += 1
            return ret
        except KeyError:
            # "{} out of work. Nomore: {}".format(self.count, self.nomore)
            if self.nomore:
                raise StopIteration()
            time.sleep(0.05)
            return self.next()  # TODO: make iterative; limit depth
        except IndexError:
            # "{} out of work. Nomore: {}".format(self.count, self.nomore)
            if self.nomore:
                raise StopIteration()
            time.sleep(0.05)
            return self.next()  # TODO: make iterative; limit depth


class Stream(object):
    """
    Represents a task that can be streamlined. Useful for doing work while
        waiting for IO.

    NOTE: May not preserve order, depending on which workers are used.
        Use .preserves_order attr to find if your Stream should preserve order.

    >>> mystream = Stream().then(
        lambda x: x ** 2,
        name="Square"
    ).then(  # [0, 1, 4, 9]
        lambda x: [i for i in range(x)],
        unpack=True,
        name=
    )
    mystream  # returns self, so you can tack on more 'thens'

    >>> mystream(range(4))
    [0, 1, 0, 1, 2, 3, 0, 1, 2, 3, 4, 5, 6, 7, 8]

    >>> mystream.errors
    {}

    >>> mystream.preserves_order
    True

    >>> mystream.then(
        lambda x: 1.0 / x,
        name="Reciprocal"
    )
    mystream

    >>> mystream(range(4))
    [1, 1, 2, 3, 1, 2, 3, 4, 5, 6, 7, 8]

    >>> mystream.errors
    {
        "Reciprocal <Worker>": [
            {"item": 0, "exception": DivideByZeroException},  # 0th index
            {"item": 0, "exception": DivideByZeroException},  # 2nd index
            {"item": 0, "exception": DivideByZeroException},  # 6th index
        ]
    }
    """
    def __init__(self, *workers, **kwargs):
        self.workers = []
        self.workline = []
        for worker in workers:
            self.then(worker, **kwargs)
        self.errors = {}

    # TODO: make add, iadd work with copies and stuff
    # def __add__(self, stream):
    #     for worker in stream.workers:
    #         self.then(worker)

    def then(self, worker, name=None, use_as=worker_types.Worker,
             unpack=None, instances=None):
        """
        Adds worker downstream. If unpack, results of worker will become
            individual items when tossed downstream.

        If worker variable is not already a worker, use_as to set the type of
            worker to use (i.e. use_as=IOWorker).

        Name (None uses default) to set the name of the worker,
            used for error logging reasons. (Is the key in the self.errors)

        Unpack (None uses Worker's default) handles a list given by the worker:
            if True, each item enters the Stream's workflow separately
                ex: a cookie-cutter, which takes 1 dish of dough and makes 12
                    gingerbread-man cookies. If unpack=True, each cookie will
                    be added to the work queue as separate tasks.
            if False, returned lists will be kept as lists.
                ex: an order-fulfiller takes 1 order and gives a list of books.
                    If unpack=False, then the list of books will stay 'packed'
                    together in the stream and not separate.

        If applicable, instances will decide how many parallel entities should
            spawned to take care of this task (like threads or processes).

        Returns this stream, so you can chain on more workers.
        """
        w = worker
        if not isinstance(w, worker_types.Worker):
            w = use_as(worker)
            if unpack is not None:
                w.unpack = unpack
        if name:
            w.error_key = name
        if instances:
            w.instances = instances

        self.workers.append(w)
        return self

    @property
    def preserves_order(self):
        return all(w.PRESERVES_ORDER for w in self.workers)

    def __call__(self, work, accumulate_errors=False):

        #
        # TODO: clean-up the case where work is a single item...
        #       (is part of making Streams in Streams a decent idea)
        #

        # If I'm not getting a list of tasks
        if not hasattr(work, "__iter__"):
            work = [work]
            if len(self.workline) - 1 is not len(self.workers):
                self.workline = [[] for w in self.workers]  # clear workline
                self.workline.append([])
                self.workline[0] = work

        # If I'm getting a bunch of tasks:
        else:
            if not accumulate_errors:
                self.errors = {}  # clear errors cache (from previous runs)

            self.workline = [[] for w in self.workers]  # clear workline
            self.workline.append([])  # adding results queue at the end
            self.workline[0] = work

        # Set up Tricklers
        self.workline = map(
            lambda l: l if isinstance(l, Trickle) else Trickle(l),
            self.workline
        )
        self.workline[0].nomore = True  # no more input in Tricker 0

        # print "Before: {}".format(self.workline)

        tapestry = [threading.Thread(**{
            "target": self.workers[i],
            "args": (self.workline[i], self.workline[i + 1], self.errors)
        }) for i in range(len(self.workers))]  # prepare worker threads
        [t.start() for t in tapestry]  # start worker threads
        [t.join() for t in tapestry]  # wait for all threads to finish

        # print "After: {}".format(self.workline)

        results = self.workline[-1].work  # return results queue
        return results


if __name__ == "__main__":
    import requests

    @worker_types.IOWorker
    def square(x):
        # SQUARING IS HARD! I'll make a server do it.
        print "{}: SEND TO SQUARE SERVER".format(x)
        url = "https://web-small-task-portfolio-semimajor.c9users.io/square/?val={}".format(x)
        result = float(requests.get(url).text)
        print "{}: RECEIVE FROM SQUARE SERVER".format(x)
        return result

    @worker_types.ThreadWorker
    def roots(x):
        print "{}: ROOTING {}".format(int(x ** .5), x)
        return [x ** .5, x ** (1. / 3)]

    mystream = Stream(
        square
    ).then(
        roots
    ).then(
        int
    )
    print "This stream does {}preserve order.".format(
        "" if mystream.preserves_order else "not "
    )
    print mystream(range(50))
    print mystream.errors
