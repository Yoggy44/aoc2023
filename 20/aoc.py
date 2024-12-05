import functools, time, copy
import re
#import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        self.lines = input_string.split("\n")

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix="\n"):
        print("")


m = Maze('inputest', "part 1")
m.solve()

m = Maze('inputest2', "part 1")
m.solve()


m = Maze('input', "part 1")
#m.solve()

m = Maze('inputest', "part 2")
#m.solve(True)

m = Maze('input', "part 2")
#m.solve(True)
