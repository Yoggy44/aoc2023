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
        self.grid=[[c for c in l] for l in lines]
        self.empty = []
        self.emptx = []
        self.galax = []
        for y, row in enumerate(self.grid):
            if '#' not in row: self.empty.append(y)
            for x in range (len(self.grid[0])):
                if self.grid[y][x] == '#': self.galax.append((x,y))
        for x in range (len(self.grid[0])):
            if '#' not in [self.grid[y][x] for y in range(len(self.grid))]: self.emptx.append(x)

    def dist(self, xy1, xy2, exp):
        x1, y1 = xy1
        x2, y2 = xy2
        dx = 0
        dy = 0
        for vx in self.emptx:
            if min(x1,x2)<vx<max(x1,x2): dx += exp-1
        for vy in self.empty:
            if min(y1,y2)<vy<max(y1,y2): dy += exp-1
        #print("between",xy1,"and",xy2,"dist=",abs(x2-x1)+abs(y1-y2)+dx+dy, "dinit", abs(x2-x1)+abs(y1-y2), "dx", dx, "dy", dy)
        return abs(x2-x1)+abs(y1-y2)+dx+dy

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        #self.display()
        for ig, g in enumerate(self.galax):
            for jg in range(ig+1, len(self.galax)):
                self.soluce += self.dist(g, self.galax[jg], 1000000 if part2 else 2)
        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix="\n"):
        print("\n".join((map(lambda li: "".join([l for l in li]), self.grid))))
        print("rows",self.empty)
        print("cols",self.emptx)
        print("Galaxies", self.galax)


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)

