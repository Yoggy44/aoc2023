import functools, time, copy
import re
import math
from itertools import combinations
#import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        lines = input_string.split("\n")
        self.clouds = []
        for l in lines:
            report, counts = l.split(' ')
            self.clouds.append({'report': report, "groups":[int(c) for c in counts.split(',')]})

    def group(self, s):
        return list(map(lambda c: len(c), re.findall('#+', s)))

    def possib(self, l, part2):
        nb = 0
        cib = functools.reduce(lambda c,t:c+t, l['groups']*(1+4*part2), 0)
        act = ('?'.join([l['report'] for _ in range(1+4*part2)])).count('#')
        inc = ('?'.join([l['report'] for _ in range(1+4*part2)])).count('?')
        #print (l['report'], '#', cib-act, '?', inc)
#        combin = int(math.factorial(inc)/(math.factorial(cib-act)*math.factorial(inc-cib+act)))
        for comb in combinations([i for i in range(inc)], cib-act):
            combi = ["#" if c in comb else "." for c in range(inc)]
            test = "".join([combi.pop(0) if c=="?" else c for c in l['report']])
            #print("comb", comb, "combi", combi, "test", test)
            if self.group(test) == l['groups']:
                nb += 1
        return nb

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        for l in self.clouds:
            self.soluce += self.possib(l, part2)
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