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
        self.hands = [{"cards": l.split(" ")[0], "bid": int(l.split(" ")[1]), "tipe": self.tipe(l.split(" ")[0], "2" in part)} for l in lines]

    def strong(self, hand, part2 = False):
        if part2: return str.translate(hand, str.maketrans("AKQT98765432J", "MLKJIHGFEDCBA"))
        return str.translate(hand, str.maketrans("AKQJT98765432", "MLKJIHGFEDCBA"))

    def tipe(self, hand, part2 = False):
        main = {h: hand.count(h) for h in set(hand)}
        if len(main) == 1: return 6 # 5 of a kind
        if len(main) == 2:
            if part2 and "J" in main.keys(): return 6
            if list(main.values())[0] in [1,4]:
                return 5 # 4 of a kind
            else: return 4 # Full House
        if max(main.values()) == 3:
            if part2 and "J" in main.keys(): return 5
            return 3 # 3 of a kind
        if max(main.values()) == 2 and len(main) == 3:
            if part2 and "J" in main.keys():
                if main["J"] == 2 : return 5
                else: return 4
            return 2 # double pair
        if max(main.values()) == 2:
            if part2 and "J" in main.keys(): return 3
            return 1 # one pair
        if part2 and "J" in main.keys(): return 1    
        return 0 # Nothing

    def solve(self, part2 = False):
        start_time = time.time()        
        self.soluce = 0
        for rank, h in enumerate(sorted(self.hands, key=lambda h:str(h["tipe"])+self.strong(h["cards"], part2))):
#            print(h["cards"], h["tipe"])
            self.soluce += (rank+1)*h["bid"]
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
