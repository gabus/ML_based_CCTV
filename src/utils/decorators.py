import time


def loop_for_sec(**kwargs):
    """
    Decorator which will keep executing function for x amount of seconds

    Required argument:
        'seconds' int|float

    Usage:
        @loop_for_sec(seconds=3)
        def some_function(a, b):
            print("test_fun executed")

        some_function(1, 2)

    Response is combined in an array. Loop through to get back each execution result.
    If function doesn't have return, array of None is returned: [None, None, None, None]
    Number of None is how many times it's been executed.
    """

    if 'seconds' not in kwargs.keys():
        raise Exception("loop_for_sec decorator requires 'seconds' argument")

    def function_caller(func):

        def function_argument_proxy(*args):
            res = []
            start = time.time()
            looping_time = kwargs['seconds']
            while start + looping_time > time.time():
                res.append(func(*args))
            return res

        return function_argument_proxy
    return function_caller
