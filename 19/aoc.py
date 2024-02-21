import functools, time, copy
import re
#import numpy as np

ACC = 'A'
REJ = 'R'
RUL = 'r'
NEXT = 'n'
X = 'x'
M = 'm'
A = 'a'
S = 's'
XMAS = (X,M,A,S)
GT = '>'
LT = '<'
OP = (GT,LT)
TYP = 'typ'
RAT = 'rat'
OPE = 'ope'
VAL = 'val'
NEX = 'nex'
OK = "ok"
KO = "ko"
CHAIN = 'ch'
MIN = 'm'
MAX = 'M'

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        lines = input_string.split("\n")
        self.wf = {}
        self.parts = []
        for l in lines:
            if len(l)==0: continue
            if l[0] != "{":
                l = l[:-1].split("{")
                key = l[0]
                self.wf[key] = []
                for r in l[1].split(","):
                    if r in (ACC,REJ):
                        self.wf[key].append({TYP:r})
                    else:
                        if GT not in r and LT not in r:
                            self.wf[key].append({TYP:NEXT, NEX:r})
                            continue
                        rule =  r.split(':')
                        rat = r[0]
                        assert rat in XMAS
                        ope = r[1]
                        assert ope in OP
                        valnex = r[2:].split(":")
                        val = int(valnex[0])
                        nex = valnex[1]
                        self.wf[key].append({TYP:RUL, RAT:rat, OPE:ope, VAL:val, NEX:nex})
            else:
                rates = {}
                for r in l[1:-1].split(","):
                    rates[r[0]] = int(r[2:])
                self.parts.append(rates)

    def next(self, wf, p):
        for r in wf:
            if r[TYP] in (REJ, ACC): return r[TYP]
            if r[TYP] == NEXT: return r[NEX]
            # RUL
            if r[OPE] == GT:
                if p[r[RAT]] >  r[VAL]: return r[NEX]
            elif p[r[RAT]] < r[VAL]: return r[NEX]

    def makegraph(self):
        self.accepted = []
        queue = [{CHAIN:[], NEX: 'in'}]
        while len(queue) > 0:
            q = queue.pop()
            ch = q[CHAIN]
            wf = self.wf[q[NEX]]
            for r in wf:
                if r[TYP] == RUL:
                    chOK = ch + [{RAT:r[RAT], OPE:r[OPE], VAL:r[VAL]}]
                    if r[NEX] == ACC:
                        self.accepted.append(chOK)
                    elif r[NEX] != REJ:
                        queue.append({CHAIN:chOK, NEX: r[NEX]})
                    ch = ch + [{RAT:r[RAT], OPE:GT if r[OPE]==LT else LT, VAL:r[VAL]+(1 if r[OPE]==GT else -1)}]
                    continue
                elif r[TYP] == ACC:
                    self.accepted.append(ch)
                    continue
                elif r[TYP] == NEXT:
                    queue.append({CHAIN:ch, NEX: r[NEX]})
                    continue
                assert r[TYP] == REJ
#        for a in self.accepted:
#            print(", ".join([r[RAT]+r[OPE]+str(r[VAL]) for r in a]))

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        if not part2:
            for p in self.parts:
                wfkey = 'in'
                while wfkey not in (ACC, REJ):
                    wfkey = self.next(self.wf[wfkey], p)
                if wfkey == ACC:
                    for x in XMAS: self.soluce += p[x]
        else:
            self.makegraph()
            for a in self.accepted:
                rang = {X:{MIN:1,MAX:4000}, M:{MIN:1,MAX:4000}, A:{MIN:1,MAX:4000}, S:{MIN:1,MAX:4000}}
                for r in a:
                    if r[OPE] == GT: rang[r[RAT]][MIN] = max(rang[r[RAT]][MIN], r[VAL]+1)
                    else: rang[r[RAT]][MAX] = min(rang[r[RAT]][MAX], r[VAL]-1)
                nb = 1
                for xmas in XMAS:
                    nb *= (rang[xmas][MAX]-rang[xmas][MIN]+1 if rang[xmas][MAX]>=rang[xmas][MIN] else 0)
                self.soluce += nb
        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix="\n"):
        print(self.wf)
        print("")
        print(self.parts)


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
