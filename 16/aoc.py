import functools, time, copy
import re
#import numpy as np

X = "x"
Y = "y"
DIR = "dir"


class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        self.grid = input_string.split("\n")

    def next(self, ray, rays):
        if 0 > ray[X] or ray[X] >= len(self.grid[0]) or 0 > ray[Y] or ray[Y] >= len(self.grid):
            return None
        if self.grid[ray[Y]][ray[X]] == '.' or (self.grid[ray[Y]][ray[X]] == "-" and ray[DIR][0]) \
                                            or (self.grid[ray[Y]][ray[X]] == "|" and ray[DIR][1]):
            return {X: ray[X]+ray[DIR][0] , Y:ray[Y]+ray[DIR][1], DIR:ray[DIR]}
        if self.grid[ray[Y]][ray[X]] in '\/':
            dif = -1 if self.grid[ray[Y]][ray[X]] == '/' else 1
            dir = (ray[DIR][1] * dif, ray[DIR][0] * dif)
            return {X: ray[X]+dir[0] , Y:ray[Y]+dir[1], DIR:dir}
        if self.grid[ray[Y]][ray[X]] in '-|':
            rays.append({X: ray[X]+ray[DIR][1] , Y:ray[Y]+ray[DIR][0], DIR:(ray[DIR][1], ray[DIR][0])})
            return {X: ray[X]-ray[DIR][1] , Y:ray[Y]-ray[DIR][0], DIR:(-ray[DIR][1], -ray[DIR][0])}
        assert False

    def nrj(self, initray):
        energized = {} # {(x,y):[(dirx,diry)])"}
        rays = [initray]
        while (rays):
            r = rays.pop()
            finished = (0 > r[X] or r[X] >= len(self.grid[0]) or 0 > r[Y] or r[Y] >= len(self.grid))
            while (not finished):
                assert r[X] >= 0 and r[Y] >= 0
                if (r[X], r[Y]) not in energized.keys(): energized[(r[X], r[Y])] = [r[DIR]]
                elif r[DIR] in energized[(r[X], r[Y])] : finished = True
                else: energized[(r[X], r[Y])].append(r[DIR])
                if not finished:
                    r = self.next(r, rays)
                    finished = (r == None) or (0 > r[X] or r[X] >= len(self.grid[0]) or 0 > r[Y] or r[Y] >= len(self.grid))
        return len(energized)

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0

        if part2:
            rays = [{X:x,                  Y:0,                DIR:(0 , 1)} for x in range(len(self.grid[0]))] \
                 + [{X:x,                  Y:len(self.grid)-1, DIR:(0 ,-1)} for x in range(len(self.grid[0]))] \
                 + [{X:0,                  Y:y,                DIR:( 1, 0)} for y in range(len(self.grid))] \
                 + [{X:len(self.grid[0])-1,Y:y,                DIR:(-1, 0)} for y in range(len(self.grid))]
        else:
            rays = [{X:0,Y:0,DIR:(1,0)}] # {X:x, Y:y, DIR:(dirx,diry))
        for initray in rays:
            self.soluce = max(self.soluce, self.nrj(initray))

        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, nrj, prefix="\n"):
        grid = [["?" for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                grid[y][x] = "." if (x,y) not in nrj.keys() else "#"
        print("\n".join("".join(l) for l in self.grid))
        print("\n")
        print("\n".join("".join(l) for l in grid))
        print("\n".join("".join(l) for l in grid).count("#"))
        print(nrj)


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
