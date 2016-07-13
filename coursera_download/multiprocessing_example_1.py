from multiprocessing import Pool, cpu_count, freeze_support
from multiprocessing.pool import ApplyResult

class Myclass(object):

    def __init__(self, nobj, workers=cpu_count()):
        pass

    def go(self, nobj, workers=cpu_count()):
        print "Constructor ..."
        # multiprocessing
        pool = Pool(processes=workers)
        async_results = [ pool.apply_async(self, (i,)) for i in range(nobj) ]
        pool.close()
        # waiting for all results
        map(ApplyResult.wait, async_results)
        lst_results=[r.get(timeout=1000) for r in async_results]
        print lst_results

    def __call__(self, i):
        return self.process_obj(i)

    def __del__(self):
        print "... Destructor"

    def process_obj(self, i):
        print "obj %d" % i
        return "result"


if __name__ == '__main__':
    freeze_support()
    m = Myclass(nobj=8, workers=3)
    m.go(nobj=8, workers=3)
# problem !!! the destructor is called nobj times (instead of once), 
# **and** results are empty !