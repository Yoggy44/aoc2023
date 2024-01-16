import functools, time, copy
import re
import functools
#import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        lines = input_string.split("\n")
        self.pattern = lines.pop(0)
        lines.pop(0)
        self.routes = {}
        self.f = 0
        for l in lines:
            key, l, r = l.replace(" ","").replace("=(",",").replace(")","").split(",")
            self.routes[key.strip()]={"L":l, "R":r, "n":[[] for ipat in range(len(self.pattern))]}

    def nextZ(self, pos, ipat):
        if self.routes[pos]["n"][ipat] != []: return self.routes[pos]["n"][ipat]
        prof = 0
        temp = [pos]
#        print (" NexxtZ", pos, "ipat", ipat)
        while True:
            pos = self.routes[pos][self.pattern[(ipat+prof) % len(self.pattern)]]
            prof += 1
            ipatmod = (ipat+prof) % len(self.pattern)
            npos = self.routes[pos]["n"][ipatmod]
    #        print ("  checking pos", pos, "cache nextZ", npos, "pat ind", ipat+prof)
    #        assert pos !='XXX'
            temp.append(pos)
            if pos[-1] == 'Z' or npos != []:
                if pos[-1] != 'Z':
   #                 print ("   found in cache of (pos=", pos, ",",prof,") =", npos,"prev temp =",temp)
                    temp += npos
  #                  print ("     new temp",temp)
                assert temp != []
                assert temp[prof:] != []
                for i in range(prof):
                    ipatmod = (ipat+i)%len(self.pattern)
 #                   print ("   add Cache for (pos=",temp[i], ", ipat=",ipatmod, ")=",temp[i+1:])
                    self.routes[temp[i]]["n"][ipatmod] = copy.copy(temp[i+1:])
                    self.f +=1
                    if self.f % 10000 ==0:
                        k0 = map(lambda r: self.routes[r]["n"],self.routes)
                        k1 = functools.reduce(lambda c,t: c+t,k0, [])
                        k = functools.reduce(lambda c,t:(c[0]+1, c[1]+len(t), c[2]+(len(t)>0)), k1,(0,0,0))                 
                        print(". cachesize", k)
                return temp[1:]

    def nextZ2(self, posi):
        pos, prof = posi
        while True:
            pos = self.routes[pos][self.pattern[(prof) % len(self.pattern)]]
            prof += 1
            if pos[-1] == 'Z':
                return (pos, prof)

    def findrecur(self, pos):
        end = False
        ipat=0
        suite = [(pos,0)]
        while not end:
            nextz = self.nextZ2(suite[-1]) 
            suite.append(nextz)
            for p,dist in suite:
                
                if p == nextz[0] and (dist-nextz[1]) % len(self.pattern) == 0:
                    end = True
                    first = p
                    break
#        print ("recur of '",pos,"' is",suite,"with",len(suite),"milestone starting at",p)
        return (suite,p)

    def decomp(self,n):
        L = dict()
        k = 2
        while n != 1:
            exp = 0
            while n % k == 0:
                n = n // k
                exp += 1
            if exp != 0:
                L[k] = exp
            k = k + 1
            
        return L

    def _ppcm(self,a,b):
        Da = self.decomp(a)
        Db = self.decomp(b)
        p = 1
        for facteur , exposant in Da.items():
            if facteur in Db:
                exp = max(exposant , Db[facteur])
            else:
                exp = exposant
            p *= facteur**exp
        for facteur , exposant in Db.items():
            if facteur not in Da:
                p *= facteur**exposant
        return p

    def ppcm(self, L):
        while len( L ) > 1:
            a = L[-1]
            L.pop()
            b = L[-1]
            L.pop()
            L.append( self._ppcm(a,b) )
            
        return L[0]

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        if not part2:
            pos="AAA"
            while pos != "ZZZ":
                pos = self.routes[pos][self.pattern[self.soluce % len(self.pattern)]]
                self.soluce +=1
        else:
            pos = []
            for r in self.routes.keys():
                if r[-1] == 'A': pos.append(self.findrecur(r))
            end = True
            l = [p[0][-1][1] for p in pos]
            self.soluce =self.ppcm(l)
                
#                 if minjump == maxjump: end = True 
#  #               print ("ms=",self.soluce,"jumping of", minjump, "end?",end)
#                 self.soluce += minjump
#                 for ip in range(len(pos)):
#                     newpos = pos[ip][1][minjump-1]
#                     pos[ip] = (newpos, self.nextZ(newpos, self.soluce % len(self.pattern)))
# #                    print("-- Newpos(", ip, ") after ms=", self.soluce, "is", pos[ip])
#                 if debug: print(self.soluce)

        print (self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix="\n"):
        print("")


m = Maze('inputest', "part 1")
m.solve()

m = Maze('inputest2', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest3', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
