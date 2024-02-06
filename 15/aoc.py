import functools, time, copy
import re
#import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        self.sequence = input_string.split(",")
        self.boxes = [[] for _ in range(256)]

    def hash(self, s):
        r = 0
        for c in s:
            r += ord(c)
            r = (r * 17) % 256
        return r

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        for seq in self.sequence:
            if not part2:
                self.soluce += self.hash(seq)
                assert seq[-1] == "-" or seq[-2] == "="
            else:
                if seq[-1] == "-": 
                    label = seq[:-1]
                    b = self.hash(label)
                    for i, (l, v) in enumerate(self.boxes[b]) :
                        if l == label:
                            self.boxes[b].pop(i)
                            break
                else:
                    label = seq[:-2]
                    b = self.hash(label)
                    found = False
                    for i, (l, v) in enumerate(self.boxes[b]) :
                        if l == label:
                            self.boxes[b][i] = (l, int(seq[-1]))
                            found = True
                            break
                    if not found:
                        self.boxes[b].append((label, int(seq[-1])))
        if part2:
            for i, b in enumerate(self.boxes):
                for j, (l,v) in enumerate(b):
                    self.soluce += (i+1) * (j+1) * v

        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix="\n"):
        for i in range(len(self.boxes)):
            if len(self.boxes[i])>0:
                print("Box",str(i)+":", " ".join(["["+l+" "+str(v)+"]" for (l,v) in self.boxes[i]]))


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
