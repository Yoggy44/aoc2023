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
        self.win = []
        self.draw = []
        self.fact = []
        r = re.compile("[0-9]+")
        for l in lines:
            l = l.split(": ")[1]
            t = l.split(" | ")
            self.win.append((r.findall(t[0])))
            self.draw.append((r.findall(t[1])))
            self.fact.append(1)

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        for i in range(len(self.draw)):
            s = 0
            for d in self.draw[i]:
                if d in self.win[i]: s += 1
            if s > 0:
                if part2:
                    for j in range(i+1, min(len(self.draw), i+1+s)): self.fact[j] += self.fact[i]
                else:
                    self.soluce += int(math.pow(2, s-1))
            if part2:
                self.soluce += self.fact[i]

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
