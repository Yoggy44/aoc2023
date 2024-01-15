import functools, time, copy
import re
import math
#import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        lines = input_string.split("\n")
        p  = re.compile("[0-9]+")
        if "2" in part:
            self.times = p.findall(lines[0].replace(" ", ""))
            self.dists = p.findall(lines[1].replace(" ", ""))
        else:
            self.times = p.findall(lines[0])
            self.dists = p.findall(lines[1])

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 1
        for i in range(len(self.times)):
            b = int(self.times[i])
            c = int(self.dists[i])
            delta = b*b-4*c
            x1 = (b - math.sqrt(delta))/2
            if float(int(x1)) == x1: x1 += 1.0
            x2 = (b + math.sqrt(delta))/2
            if float(int(x2)) == x2: x2 -= 1.0
#            print("x1", x1,"x2",x2, "nb", math.trunc(x2)-math.ceil(x1)+1)
            self.soluce = self.soluce * (math.trunc(x2)-math.ceil(x1)+1) 
        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix="\n"):
        print("")


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
