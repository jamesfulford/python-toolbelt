
from multiprocessing import Pool


def fibonacci(x):
    if x in (0, 1):
        return 1
    return fibonacci(x - 1) + fibonacci(x - 2)


inputs = range(30)
processes = 8


# print "Single"  # 3.0, 2.5, 2.4, 2.5, 2.5
# results = map(fibonacci, inputs)
# print results


# print "Multi", len(inputs)  # 1.4, 1.4, 1.4, 1.4, 1.4
# pool = Pool(processes=len(inputs))
# results = [pool.apply_async(fibonacci, args=(i,)) for i in inputs]
# results = [r.get() for r in results]
# print results


def parallel(*fns):
    pool = Pool(processes=8)

    def do(arg, **kwargs):
        for fn in fns:
            result = pool.apply_async(fn, args=(arg,), kwds=kwargs)
            result.get()

# def parallel(fn, chores):
#     pool = Pool(processes=8)
#     result = pool.apply_async(fn, chores)
#     return result.get()


# chores = [1, 3, 8]
# print chores
# print parallel(lambda x: x ** 2, chores)
