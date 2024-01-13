import functools, time, copy
import re
import math

#import numpy as np
DST = 'dst'
SRC = 'src'
LONG = 'long'

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        lines = input_string.split("\n")
        ss = lines.pop(0).split(": ")[1].split(" ")
        if '1' in part:
            self.seeds = [(int(s),1) for s in ss]
        else:
            self.seeds = [(int(ss[i]), int(ss[i+1])) for i in range(0,len(ss),2)]
        lines.pop(0)
        self.types = ['ss', 'sf', 'fw', 'wl', 'lt', 'th', 'hl']
        self.conv = {}
        i = -1
        for l in lines:
            if l == "" and i >= 0:
                self.conv[self.types[i]] = curmap
                continue
            if l[0] not in '0123456789':
                i += 1
                curmap = []
                continue
            s = l.split(' ')
            curmap.append({DST: int(s[0]), SRC: int(s[1]), LONG: int(s[2])})
        self.conv[self.types[i]] = curmap

    def convert(self, s, c):
        return (c[DST] + s[0] - c[SRC], s[1])

    def intersect(self, s1, s2):
        if s1[0] > s2[0] + s2[1] -1 or s1[0] + s1[1] -1 < s2[0]:
            return None
        return (max(s1[0], s2[0]), min(s2[0] + s2[1] -1, s1[0] + s1[1] -1)-max(s1[0], s2[0])+1)
        
    def remain(self, segs, rem):
        s = []
        # check
        assert rem[0]<=segs[0]+segs[1]-1 and rem[0]+rem[1]-1>=segs[0]
        if segs != rem:
            if segs[0] < rem[0] :
                s.append((segs[0], rem[0]-segs[0]))
            if segs[0]+segs[1] > rem[0]+rem[1] :
                s.append((rem[0]+rem[1], segs[0]+segs[1]-rem[0]-rem[1]))
        return s

    def check(self, tab):
        lr=0
        for _,l in tab: lr += l
        return lr

    def rconvert(self, s, c):
        return (c[SRC] + s[0] - c[DST], s[1])

    def getseed(self, soluce, tinit, debug=False):
        s = (soluce, 1)
        for ti in range(tinit, -1, -1):
            t = self.types[ti]
            for c in self.conv[t]:
                inters = self.intersect(s, (c[DST], c[LONG]))
                if inters != None:
                    s = self.rconvert(inters, c)
                    break
        found = False
        for ss in self.seeds:
            if ss[0] <= s[0] < ss[0]+ss[1]:
                found = True
                ssi = ss
                break
        if not found:
            print("seed not found", self.types[tinit], soluce)
        assert found
        return s[0]

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = -1
        debug = False
        for ss, long in self.seeds:
            ssegms = [(ss,long)]
            dsegms = []
            for ti in range(len(self.types)):
                t = self.types[ti]
                for c in self.conv[t]:
                    tempss = copy.copy(ssegms)
                    for s,l in ssegms:
                        inters = self.intersect((s,l), (c[SRC], c[LONG]))
                        if inters != None:
                            dsegms.append(self.convert(inters, c))
                            tempss.remove((s,l))
                            tempss += self.remain((s,l), inters)
                            assert self.check(tempss) + self.check(dsegms) == long
                    ssegms = copy.copy(tempss)
                ssegms += dsegms
                dsegms = []
                # Check
                assert self.check(ssegms) == long
                for i in ssegms:
                    self.getseed(i[0], ti, debug = debug)
            for s,l in ssegms:
                if self.soluce < 0:
                    self.soluce = s
                else: self.soluce = min(self.soluce, s)
        inits = self.getseed(self.soluce, len(self.types)-1)
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
#30641708 toolow