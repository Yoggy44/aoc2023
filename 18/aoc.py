import functools, time, copy
import re
#import numpy as np

DIR = 'dir'
LEN = 'len'
DIR2 = 'dir2'
LEN2 = 'len2'

E='R'
W='L'
N='U'
S='D'
DIRS=[E,S,W,N]

VIDE = ' '
NS='│'
EW='─'
NE='└'
NW='┘'
SE='┌'
SW='┐'

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        self.moves = [{DIR:c.split(" ")[0], LEN:int(c.split(" ")[1]), DIR2:self.decodedir(c.split(" ")[2]), LEN2:self.decodelen(c.split(" ")[2])} for c in input_string.split("\n")]

    def decodedir(self, hex):
        return DIRS[int(hex[-2])]
    def decodelen(self, hex):
        return int(hex[2:7], 16)

    def dig(self, part2 = False):
        x = y = xmin = ymin = xmax = ymax = 0
        for m in self.moves:
            if m[DIR] == E:
                x+=m[LEN]
                if x > xmax: xmax = x
            if m[DIR] == W:
                x-=m[LEN]
                if x < xmin: xmin = x
            if m[DIR] == S:
                y+=m[LEN]
                if y > ymax: ymax = y
            if m[DIR] == N:
                y-=m[LEN]
                if y < ymin: ymin = y
        self.grid = [[VIDE for _ in range(xmax-xmin+1)] for _ in range(ymax-ymin+1)]
        x,y,dir = (-xmin, -ymin, self.moves[-1][DIR])
        for m in self.moves:
            dx = dy = 0
            if m[DIR] == E:
                assert dir not in (W,E)
                dx=1
                c = NE if dir == S else SE
            if m[DIR] == W:
                assert dir not in (W,E)
                dx=-1
                c = NW if dir == S else SW
            if m[DIR] == S:
                assert dir not in (N,S)
                dy=1
                c = SW if dir == E else SE
            if m[DIR] == N:
                assert dir not in (N,S)
                dy=-1
                c = NW if dir == E else NE
            dir = m[DIR]
            self.grid[y][x] = c
            x,y=(x+dx,y+dy)
            for _ in range(m[LEN]-1):
                self.grid[y][x] = EW if m[DIR] in (E,W) else NS
                x,y=(x+dx,y+dy)

    def dig2(self, part2 = False):
        self.path = {}
        x = y = xmin = ymin = xmax = ymax = 0
        dir=self.moves[-1][DIR2]
        for m in self.moves:
            dx = dy = 0
            if m[DIR2] == E:
                if x > xmax: xmax = x
                dx=1
                c = NE if dir == S else SE
            if m[DIR2] == W:
                if x < xmin: xmin = x
                dx=-1
                c = NW if dir == S else SW
            if m[DIR2] == S:
                if y > ymax: ymax = y
                dy=1
                c = SW if dir == E else SE
            if m[DIR2] == N:
                if y < ymin: ymin = y
                dy=-1
                c = NW if dir == E else NE
            dir = m[DIR2]
            self.path[(x,y)] = c
            x,y=(x+dx*m[LEN2],y+dy*m[LEN2])
        assert (x,y) == (0,0)
        ms = functools.reduce(lambda c,xy:(c[0]+[xy[0]], c[1]+[xy[1]]), self.path.keys(), ([], []))
        self.milestones = (sorted(set(ms[0]))), list(sorted(set(ms[1])))

    def fill(self):
        for y,l in enumerate(self.grid):
            out=True
            for x,c in enumerate(l):
                if c in (NE,NW,NS): out = not out
                if c != VIDE or (c == VIDE and not out):
                    self.soluce += 1
                    if c == VIDE and not out: self.grid[y][x] = "#"

    def crossing(self, x, y):
        l = [xy[1] for xy in self.path.keys() if xy[0] == x]
        yinf = self.milestones[1][0]-1
        for yy in l:
            if yinf < yy < y : yinf = yy
        return yinf > self.milestones[1][0]-1 and self.path[(x,yinf)] in (SE, SW)

    def fill2(self):
        yprev = self.milestones[1][0]
        infill = 0
        for y in self.milestones[1]:
            xprev = self.milestones[0][0]
            # Remplissage en hauteur
            #print("y",y, "infill", infill, "*", y-yprev-1)
            self.soluce += infill * (y - yprev -1)            
            inside = False
            infill = 0
            s_inside = False
            cross = None
            for x in self.milestones[0]:
                # add inter-delta if inside
                infill += s_inside * (x - xprev - 1) 
                #if s_inside: print("adding width between",xprev, "and", x, "with s_inside")
                if (x,y) in self.path.keys():
                    #if inside or cross != None: print("- segment inside or inpath width-1 between", xprev,"and",x)
                    self.soluce += (inside or cross != None) * (x - xprev - 1) 
                    # Check if chanfgement de sens
                    if cross == None:
                        cross = S if self.path[(x,y)] in (SW,SE) else N
                    elif (cross == S and self.path[(x,y)] in (SW,SE)) or (cross == N and self.path[(x,y)] in (NW,NE)):
                        cross = None
                    else:
                        cross = None
                        inside = not inside
                    # add 1 because xy in path
                    #print("- line +1 because path in x=",x)
                    self.soluce += 1
                    if self.path[(x,y)] in (SE, SW):
                        infill += 1
                        #print("adding 1 because xy=", (x,y), "is SE or SW")
                        s_inside = not s_inside
                    else:
                        infill += s_inside
                        #if s_inside: print("adding 1 because s_inside", (x,y))
                else:
                    #if inside or cross != None: print("- segment inside or inpath width-1 between", xprev,"and",x)
                    self.soluce += (inside or cross != None) * (x - xprev - 1) 
                    # change inside if crossing |
                    if self.crossing(x,y):
                        inside = not inside
                        assert cross == None
                        s_inside = not s_inside
                        infill += 1
                        #print("adding 1 because xy=", (x,y), "is crossing")
                        self.soluce += 1
                        #print("- line +1 because crossing path in x=", x)
                    else:
                        infill += s_inside
                        #if s_inside: print("adding 1 because s_inside", (x,y))
                        # add 1 xy out of path if inside
                        self.soluce += inside or cross != None
                        #if inside or cross != None: print("- line +1 because inside in x=", x)
                xprev = x
            yprev = y
        assert infill==0
        return

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        if not part2:
            self.dig()
            self.fill()
        else:
            self.dig2()
            self.fill2()
        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix="\n"):
        for l in self.grid:
            print("".join(c for c in l))


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
