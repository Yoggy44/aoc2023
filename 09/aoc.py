import functools, time, copy
import re, math
#import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        lines = input_string.split("\n")
        self.d = [[[int(x) for x in l.split(' ')]] for l in lines]

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        for l in range(len(self.d)):
            for j in range(1, len(self.d[l][0])):
                self.d[l].append([self.d[l][j-1][i+1] - self.d[l][j-1][i] for i in range(len(self.d[l][0])-j)])
                #print ("l",l,"j",j,len(self.d[l]), self.d[l][j])
                if all(i == 0 for i in self.d[l][j]):
                        N = j
                        break
            for i in range(N):
                self.soluce += self.d[l][i][-1] if not part2 else int(math.pow(-1,i)) * self.d[l][i][0]

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
