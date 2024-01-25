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
        self.grid = [[{'tile':' ', 'stat':0} for _ in range(len(lines[0]))] for _ in range(len(lines))]
        self.gridstat = [[2 for _ in range(len(lines[0]))] for _ in range(len(lines)-1)]
        for y, l in enumerate(lines):
            for x, c in enumerate(l):
                if c == 'S':
                    self.start = (x,y)
                    self.grid[y][x]['stat'] = -1
                self.grid[y][x]['tile'] = c
        self.dirs = {'N': (0,-1), 'S': (0,1), 'E':(1,0), 'W':(-1,0)}

    def chgdir(self, tile, dir):
        if tile == 'F' and dir == 'N': return 'E'
        if tile == 'F' and dir == 'W': return 'S'
        if tile == 'L' and dir == 'S': return 'E'
        if tile == 'L' and dir == 'W': return 'N'
        if tile == '7' and dir == 'E': return 'S'
        if tile == '7' and dir == 'N': return 'W'
        if tile == 'J' and dir == 'S': return 'W'
        if tile == 'J' and dir == 'E': return 'N'
        return dir

    def depl(self, pos, dir):
        x = pos[0] + self.dirs[dir][0]
        y = pos[1] + self.dirs[dir][1]
        d = self.chgdir(self.grid[y][x]['tile'], dir)
        return ((x, y), d)

    def dirstart(self):
        if self.start[1] < len(self.grid)-1 and self.grid[self.start[1]+1][self.start[0]]['tile'] in '|LJ':
            self.grid[self.start[1]][self.start[0]]['tile'] = '|'
            return 'S'
        if self.start[0] > 0 and self.grid[self.start[1]][self.start[0]-1]['tile'] in '-FL': return 'W'
        return 'E'

    # def outstart(self):
    #     for y in range(len(self.grid)):
    #         for x in range(len(self.grid[0])):
    #             if x in (0, len(self.grid[0])-1) or y in (0, len(self.grid)-1):
    #                 if self.grid[y][x]['stat'] >= 0: return (x, y)
    #     assert False

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        lg = 1
        cur, dir = self.depl(self.start, self.dirstart())
        while not cur == self.start:
            self.grid[cur[1]][cur[0]]['stat'] = -2
            lg +=1
            cur, dir = self.depl(cur, dir)
        if not part2:
            self.soluce = (lg//2) 
        else:
            for y in range(len(self.gridstat)):
                cur = 0
                for x in range(len(self.gridstat[0])):
                    cell = self.grid[y][x]
                    self.gridstat[y][x] = cur
                    if cell['stat']<0 and cell['tile'] in 'F|7':
                        cur = 1-cur
            for y in range(1, len(self.grid)-1):
                for x in range(1, len(self.grid[0])-1):
                    if self.grid[y][x]['stat'] == 0:
                        if self.gridstat[y][x] == 1:
                            self.grid[y][x]['tile'] = 'I'
                            self.soluce += 1
                        else:
                            self.grid[y][x]['tile'] = ' '
            #self.display()
            # Parcourir tout grid, si tile = '.' et contourIn() soluce +=1
        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix="\n"):
        print("\n".join((map(lambda li: "".join([str(l) for l in li]), self.gridstat))))
        print("\n".join((map(lambda li: "".join([l['tile'] for l in li]), self.grid))))

m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest2', "part 2")
m.solve(True)

m = Maze('inputest3', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
