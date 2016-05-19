#encoding=utf8
from multiprocessing import Pool
import traceback


class MultiPool:
    def __init__(self, num=6):
        self.pool = Pool(num)
        self.jobs = []

    def addJob(self, job, *args):
        self.jobs.append((job, args))


    def waitClose(self):
        for job, args in self.jobs:
            try:
                self.pool.apply_async(job, args)
            except:
                print traceback.format_exc()

        self.pool.close()
        self.pool.join()

def func(li):
    print li

if __name__ == "__main__":
    pool = MultiPool(2)
    li = [1,2,3,4,5]
    pool.addJob(func, li)
    pool.addJob(func, li)
    pool.waitClose()
        
        
        
    
	
