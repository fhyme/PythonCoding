__author__ = 'Albert'

from multiprocessing import Pool, cpu_count, freeze_support
from multiprocessing.pool import ApplyResult

# --------- see Stenven's solution above -------------
from copy_reg import pickle
from types import MethodType

def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)


class Myclass(object):

    def __init__(self, nobj, workers=cpu_count()):

        print "Constructor ..."
        # multi-processing
        pool = Pool(processes=workers)
        async_results = [ pool.apply_async(self.process_obj, (i,)) for i in range(nobj) ]
        pool.close()
        # waiting for all results
        map(ApplyResult.wait, async_results)
        lst_results=[r.get() for r in async_results]
        print lst_results

    def __del__(self):
        print "... Destructor"

    def process_obj(self, index):
        print "object %d" % index
        return "results"


if __name__ == '__main__':
    freeze_support()
    pickle(MethodType, _pickle_method, _unpickle_method)
    Myclass(nobj=8, workers=3)
# problem !!! the destructor is called nobj times (instead of once)
