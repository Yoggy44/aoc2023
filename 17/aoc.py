import functools, time, copy
import re
#import numpy as np

E, S, W, N, R, L = ('E', 'S', 'W', 'N', 'R', 'L')

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        self.grid = input_string.split("\n")
        self.maxsol = 0
        for l in self.grid:
            for c in l:
                self.maxsol += int(c)
        self.dirs = [N, E, S, W]
        self.maxstraight = 3
        self.scores=[[self.maxsol for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        self.path=[]

    def go(self, x, y, dir, turn):
        assert dir in self.dirs
        assert turn in (R,S,L)
        if turn in (R, L): dir = self.dirs[(self.dirs.index(dir) + (1 if turn == R else -1)) % len(self.dirs)]
        x += (1 if dir == E else -1 if dir == W else 0)
        y += (1 if dir == S else -1 if dir == N else 0)
        return (x, y, dir)

    def next(self, path = [], dir = E, turns = [], score = 0):
        tries = [(path, dir, turns, score)]
        interm = time.time()
        while len(tries) > 0:
            if time.time()-interm > 1000:
                interm = time.time()
                print ("tries", len(tries), "path", len(path), "best score", self.soluce)
            path, dir, turns, score = tries.pop()
            x,y = (0,0) if len(path)==0 else path[-1]
            # Stop if higher than best score
            if score > self.soluce: continue
            # Stop if score is higher than the best known score
            if score > self.scores[y][x]+1: continue
            else: self.scores[y][x] = score
            # Stop if final position
            if (x,y) == (len(self.grid[0])-1, len(self.grid)-1):
                if score < self.soluce:
                    #print("soluce", s,"old soluce", self.soluce, "len path",len(path))
                    self.soluce = score
                    self.path = path
                continue
            # Check max straight
            nostraight = (len(turns) >= self.maxstraight and all([turns[-i-1]==S for i in range(self.maxstraight-1)]))
            # Turns
            for t in (S,L,R):
                x2, y2, dir2 = self.go(x, y, dir, t)
                if 0 <= x2 < len(self.grid[0]) and 0 <= y2 < len(self.grid) and (x2, y2) not in path and (t!=S or not nostraight):
                    newpath = path+[(x2, y2)]
                    newturns = (turns+[t])[-self.maxstraight:]
                    newscore = score + int(self.grid[y2][x2])
                    tries.append((newpath, dir2, newturns, newscore))

    def solve(self, part2 = False):
        start_time = time.time()
        x,y = (0,0)
        self.soluce = self.maxsol
        
        self.next()
        #self.display(self.path)

        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, p):
        for y,l in enumerate(self.grid):
            print("".join([(" " if (x,y) not in p else c) for x, c in enumerate(l)]), l)
        for l in self.scores:
            print(", ".join([str(s) for s in l]))

m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
#m.solve(True)

m = Maze('input', "part 2")
#m.solve(True)
