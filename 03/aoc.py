import functools, time, copy
import re
#import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        self.grid = input_string.split("\n")
        self.numbers="0123456789"

    def isAdjacent(self, x,y):
        for d in [[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1]]:
            if 0 <= x+d[0] < len(self.grid[0]) and 0 <= y+d[1] < len(self.grid) and self.grid[y+d[1]][x+d[0]] not in self.numbers+".":
                return True
        return False

    def num(self, x,y):
        while x-1 >= 0 and self.grid[y][x-1] in self.numbers:
            x -= 1
        n = int(self.grid[y][x])
        while x+1 <= len(self.grid[0])-1 and self.grid[y][x+1] in self.numbers:
            x += 1
            n = 10*n + int(self.grid[y][x])
        return n

    def isGear(self, x,y):
        nbnum = 0
        gear = 1
        for d in [[-1,0],[0,-1],[1,0],[0,1]]:
            if 0 <= x+d[0] < len(self.grid[0]) and 0 <= y+d[1] < len(self.grid):
                c = self.grid[y+d[1]][x+d[0]]
                if c in self.numbers:
                    gear = gear * self.num(x+d[0], y+d[1])
                    nbnum += 1
                elif d[0]==0:
                    for d0 in [-1,1]:
                        if 0 <= x+d0 < len(self.grid[0]) and 0 <= y+d[1] < len(self.grid):
                            c = self.grid[y+d[1]][x+d0]
                            if c in self.numbers:
                                gear = gear * self.num(x+d0, y+d[1])
                                nbnum += 1
        if nbnum == 2:
            return gear
        return 0

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0

        if not part2:
            for y in range(len(self.grid)):
                temp = 0
                enable = False
                for x in range(len(self.grid[0])):
                    c = self.grid[y][x]
                    if c in self.numbers:
                        temp = 10*temp + int(c)
                        enable = enable or self.isAdjacent(x, y)
                    if c not in self.numbers or x == len(self.grid[0])-1:
                        if enable:
                            self.soluce += temp
                        enable = False
                        temp = 0 
        else:
            for y in range(len(self.grid)):
                for x in range(len(self.grid[0])):
                    c = self.grid[y][x]
                    if c == "*":
                        self.soluce += self.isGear(x, y)

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
# too low