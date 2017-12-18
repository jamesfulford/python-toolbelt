# worker_types.py


from multiprocessing import Pool as ProcessPool
from multiprocessing.pool import ThreadPool


#
# Actual Workers, not decorators yet.
#

class Worker(object):
    """
    Wraps function which does work. When called, uses wrapped function on each
    input and outputs into buffer given.

    If wrapped function raises an exception, that item is excluded from output
    and the item is collected in error_buffer under self.error_key
    and the exception is collected under self.error_key + "_exception".

    When done ALL work, sets output_list.nomore to True.

    recip = _worker(lambda x: 1.0 / x, "reciprocal")
    work, output, error = [2, 1, 0], [], {}
    recip(work, output, error)

    # wait a bit

    >>> output
    [.5, 1.0]

    >>> error



    """
    PRESERVES_ORDER = True
    UNPACK = False
    INSTANCES = 1  # default value

    def __init__(self, fn):
        """
        Setting unpack flag will override class's default value (UNPACK), so
            results of worker will become individual items when tossed
            downstream.
        """
        self.fn = fn
        self.error_key = "{} <{}>".format(fn.__name__, self.__class__.__name__)
        self.unpack = self.__class__.UNPACK  # set default value
        self.instances = self.__class__.INSTANCES

    def process(self, work_list, output_list):
        """
        Default: single-threaded execution of work.
        Override this function for different workers.
        """
        for item in work_list:
            try:
                res = self.fn(item)
            except Exception as e:
                self.log(item, e)
            else:
                self.done(res, output_list)

    def done(self, finished_product, output_list):
        if hasattr(finished_product, "__iter__") and self.unpack:
            output_list.extend(list(finished_product))
        else:
            output_list.append(finished_product)

    def log(self, item, exception):
        self.error_buffer[self.error_key].append({
            "item": item,
            "exception": exception
        })

    def __call__(self, work_list, output_list, error_buffer):
        # Prepare for errors
        self.error_buffer = error_buffer  # for self.log function
        error_buffer[self.error_key] = error_buffer.get(self.error_key, [])

        # Delegate
        self.process(work_list, output_list)

        # Tell the next Trickler that no more is coming
        output_list.nomore = True


class ThreadWorker(Worker):
    PRESERVES_ORDER = True
    INSTANCES = 6

    def process(self, work_list, output_list):
        """
        Preserves order. If one request takes too long, the worker will
            continue but will hold up the stream.
        """
        def do(task):
            try:
                return self.fn(task)
            except Exception as e:
                self.log(task, e)
                return e

        pool = ThreadPool(self.instances)
        for result in pool.imap(do, work_list):
            if not isinstance(result, Exception):
                self.done(result, output_list)
        pool.close()
        pool.join()


class IOWorker(Worker):
    PRESERVES_ORDER = False
    INSTANCES = 12

    def process(self, work_list, output_list):
        """
        Does not preserve order, in exchange for less bottlenecking downstream.
        """
        def do(task):
            try:
                res = self.fn(task)
            except Exception as e:
                self.log(task, e)
            else:
                self.done(res, output_list)

        pool = ThreadPool(self.instances)
        pool.map(do, work_list)
        pool.close()
        pool.join()


class ProcessWorker(Worker):
    PRESERVES_ORDER = False
    INSTANCES = 4

    def process(self, work_list, output_list):
        """
        NOTE: This is not preserving order right now.
        NOTE: This also may not work.
        """
        def do(task):
            try:
                res = self.fn(task)
            except Exception as e:
                self.log(task, e)
            finally:
                self.done(res, output_list)

        pool = ProcessPool(self.instances)
        pool.map(do, work_list)
        pool.close()
        pool.join()
