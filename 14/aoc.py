import functools, time, copy
import re
#import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open(f+'.txt') as fi:
            input_string = fi.read()
        self.lines = input_string.split("\n")

    def tilt(self, tab, dir = "N"):
        # Pour chaque ligne
        if dir in ('N', 'S'):
            for i in range(len(tab)) if dir == "N" else range(len(tab)-2, -1, -1):
                # pour chaque colonne de la ligne
                for j in range(len(tab[0])):
                    # Si c'est une pierre ronde
                    if tab[i][j] == "O":
                        # on regarde ce quil y a au nord/sud
                        for k in range(i-1,-1,-1) if dir == "N" else range(i+1,len(tab)):
                            # Si c'est vide on pousse la pierre au nord/sud
                            if tab[k][j] == ".":
                                #print("Fall i",i, "j", j, "k", k)
                                tab[k] = tab[k][:j] + "O" + tab[k][j+1:]
                                # print ("tab[",k+1,"]= tab[",
                                #     k+(1 if dir == "N" else -1),
                                #     "][:",
                                #     j,
                                #     "]+'.'+tab[",
                                #     k+(1 if dir == "N" else -1),
                                #     "][",
                                #     j+1,
                                #     ":] / dir=",dir)
                                tab[k+(1 if dir == "N" else -1)] = tab[k+(1 if dir == "N" else -1)][:j] + "." + tab[k+(1 if dir == "N" else -1)][j+1:]
                            else: break
        if dir in ('E', 'W'):
            # pour chaque colonne
            for j in range(len(tab[0])) if dir == "W" else range(len(tab[0])-1, -1, -1):
                # pour chaque ligne de la colonne
                for i in range(len(tab)):
                    # Si c'est une pierre ronde
                    if tab[i][j] == "O":
                        # on regarde ce quil y a au west/east
                        for k in range(j-1,-1,-1) if dir == "W" else range(j+1,len(tab[0])):
                            # Si c'est vide on pousse la pierre au west/east
                            if tab[i][k] == ".":
                                tab[i] = tab[i][:k-(dir=="E")] + ("O." if dir == "W" else ".O") + tab[i][k+1+(dir == "W"):]
                            else: break
        return tab

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = 0
        #self.display()
        #print("\nTRAITEMENT\n")
        if part2:
            l = copy.copy(self.lines)
            olds = [self.lines]
            found = False
            i = 0
            imax = 1000000000
            while i < imax:
                #if found: print("Cycle", i+1)
                l = self.tilt(l, "N")
                l = self.tilt(l, "W")
                l = self.tilt(l, "S")
                l = self.tilt(l, "E")
                #print("\nAfter E+ cycle",i+1)
                #self.display(l)
                if not found and l in olds:
                    found = True
                    first = olds.index(l)-1
                    #print("Modulo",i-first)
                    i = imax-1 - ((imax-1-first)%(i-first))
                    #break
                olds.append(copy.copy(l))
                i += 1
            self.lines = copy.copy(l)
        else: 
            self.lines = self.tilt(self.lines)

        #self.display()
        for i,l in enumerate(self.lines):
            self.soluce += (len(self.lines)-i) * l.count("O")
        print (self.f, self.part,"lines in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, tab, prefix="\n"):
        print("\n".join(tab))


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
