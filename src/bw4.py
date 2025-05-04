#!/usr/bin/env python
#
# Black and white automata that uses four cells above, two on left and two on right but not center
#

import sys
from lib.automata import BWAutomata, Row
from bitarray import bitarray
from bitarray.util import ba2int

class FourBitRow(Row):

    def __init__(self, width):
        self.width = width
        self.edge = width - 2
        self.vals = bitarray(width)

    def __str__(self):
        return str(self.vals)

    def __repr__(self):
        return self.__str__()

    def set(self, loc, val):
        self.vals[loc] = val

    def gen_vals(self):
        ret_val = self.vals[1:3]
        ret_val.insert(0,self.vals[-1])
        ret_val.insert(0,self.vals[-2])
        yield ret_val
        ret_val = self.vals[2:4]
        ret_val.insert(0,self.vals[0])
        ret_val.insert(0,self.vals[-1])
        yield ret_val
        for loc in range(2, self.edge):
            ret_val = self.vals[loc-2:loc+3]
            ret_val.pop(2)
            yield ret_val
        ret_val = bitarray(4)
        ret_val[0] = self.vals[self.edge-2]
        ret_val[1] = self.vals[self.edge-1]
        ret_val[2] = self.vals[self.edge+1]
        ret_val[3] = self.vals[0]
        yield ret_val
        ret_val = bitarray(4)
        ret_val[0] = self.vals[self.edge-1]
        ret_val[1] = self.vals[self.edge]
        ret_val[2] = self.vals[0]
        ret_val[3] = self.vals[1]
        yield ret_val
        return

class FourBitAutomata(BWAutomata):

    def get_row(self):
        return FourBitRow(self.width)

    def calculate_it(self, algo_pattern, data):
        loc = ba2int(data)
        return algo_pattern[15-loc]

    def get_pattern(self):
        return bitarray(bin(self.algo)[2:].zfill(16))


def verify_pattern():
    row = FourBitRow(6)
    for i in range(0, 6, 2):
        row.set(i, 1)
    print(f"row: {row}")
    row_gen = row.gen_vals()
    for i in range(6):
        print(f"{i}: {next(row_gen)}")

    row = FourBitRow(6)
    row.set(2, 1)
    row.set(3, 1)
    row.set(5, 1)
    print(f"row: {row}")
    row_gen = row.gen_vals()
    for i in range(6):
        print(f"{i}: {next(row_gen)}")

def main():
    algo = int(sys.argv[1]) if len(sys.argv) > 1 else 52
    automata = FourBitAutomata(1600, 1000, algo, 'random')
    automata.run()


if __name__=='__main__':
    #main()
    verify_pattern()