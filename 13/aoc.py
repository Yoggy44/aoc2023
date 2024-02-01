import functools, time, copy
import re
#import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        lines = input_string.split("\n")
        self.pattern = []
        p=[]
        for l in lines:
            if l == "":
                self.pattern.append(p)
                p = []
                continue
            p.append(l)
        self.pattern.append(p)

    def col(self, tab, col):
        return [t[col] for t in tab]

    def diffs(self, tab1, tab2):
        if tab1 == tab2: return 0
        count = 0
        for i,c in enumerate(tab1):
            if c != tab2[i]: count += 1
            if count > 1 : return count
        return count

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        #self.display()
        for p in self.pattern:
            for v in range(len(p[0])-1):
                diffs = 0
                for delta in range(min(v+1,len(p[0])-1-v)):
                    diffs += self.diffs(self.col(p, v-delta), self.col(p, v+1+delta))
                    if (diffs > 0 and not part2) or (diffs > 1 and part2):
                        break
                if (diffs == 0 and not part2) or (diffs == 1 and part2):
                    #print ("Found Vertical", v+1)
                    self.soluce += v+1
            for h in range(len(p)-1):
                diffs = 0
                for delta in range(min(h+1,len(p)-1-h)):
                    diffs += self.diffs(p[h-delta], p[h+1+delta])
                    if  (diffs > 0 and not part2) or (diffs > 1 and part2):
                        break
                if (diffs == 0 and not part2) or (diffs == 1 and part2):
                    #print ("Found Horizontal", h+1)
                    self.soluce += 100*(h+1)
        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix="\n"):
        for i,p in enumerate(self.pattern): print ("Pattern", i,"\n", "\n".join(p))


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
