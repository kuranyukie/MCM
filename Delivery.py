from math import *
from Country import *

class Delivery :
    def __init__(self) :
        self.task = [] # form : [self.t, self.claim, self.name]


    def sort(self, task) :
        if len(task) > 1:
            task.sort(key = lambda x : x[0]) 
        return task


if __name__ == '__main__':
    d = Delivery()
    print d.sort([[3, 100, 'L'],[1, 300, 'G'],[5, 200, 'S']])
