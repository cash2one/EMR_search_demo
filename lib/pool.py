#encoding=utf8
from multiprocessing import Pool


class MultiPool:
    def __init__(self, num=6):
        self.pool = Pool(num)
        self.jobs = []

    def addJob(self, job, *args):
        self.jobs.append((job, args))


    def waitClose(self):
        for job, args in self.jobs:
            self.pool.apply_async(job, args)

        self.pool.close()
        self.pool.join()

global t
t = 100
def func():
    print t

if __name__ == "__main__":
    pool = MultiPool(2)
    pool.addJob(func)
    #pool.addJob(func)
    pool.waitClose()
        
        
        
    
	
