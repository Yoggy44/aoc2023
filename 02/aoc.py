import functools, time, copy
import re
#import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        games = input_string.split("\n")
        self.games = []
        self.colors = {'blue', 'red', 'green'}
        for g in games:
            game = []
            turns = g.split(": ")[1].split("; ")
            for t in turns:
                cubes = t.split(", ")
                turn = {} # [3 blu, 3 red]
                for c in cubes:
                    grab = c.split(" ")
                    turn[grab[1]]=int(grab[0])
                game.append(turn)
            self.games.append(game)

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        if not part2:
            bags = {'red': 12, 'green': 13, 'blue': 14} #if not part2 
            for i in range(len(self.games)):
                possible = True
                for t in range(len(self.games[i])):
                    if possible:
                        for g in self.games[i][t]:
                            if bags[g] < self.games[i][t][g]: 
                                possible = False
                                break 
                if possible:
                    self.soluce += i+1
        else:
            for i in range(len(self.games)):
                mini = {c: 0 for c in self.colors}
                for t in range(len(self.games[i])):
                    for g in self.games[i][t]:
                        if mini[g] < self.games[i][t][g]: 
                            mini[g] = self.games[i][t][g] 
                s = 1
                for c in self.colors:
                    s *= mini[c]
                self.soluce += s
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
