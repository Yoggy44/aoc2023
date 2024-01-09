import functools, time, copy
import re
#import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        self.calibs = input_string.split("\n")
        if self.calibs[-1] == "": self.calibs.pop()

    def predecode(self, s):
        changed=False
        spl = re.split(r'(one|two|three|four|five|six|seven|eight|nine|[1-9])(.*)', s)
        conv = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}
        for i in range(len(spl)):
            if spl[i] in conv.keys():
                spl[i] = conv[spl[i]]
                changed=True
        spl=re.split(r'(.*)(one|two|three|four|five|six|seven|eight|nine|[1-9])', ''.join(spl))
        for i in range(len(spl)):
            if spl[i] in conv.keys():
                spl[i] = conv[spl[i]]
                changed=True
        #if changed: print (s, '=>', ''.join(spl))
        return ''.join(spl)

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        p  = re.compile("[0-9]")
        for l in self.calibs:
            if part2: l = self.predecode(l)
            m = p.findall(l)
            self.soluce += int(m[0] + m[-1])
        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix="\n"):
        print("")


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest2', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
