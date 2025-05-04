#!/usr/bin/env python
##
## Black and white automata that uses three cells above, left, center and right
##

import sys
import argparse
from lib.automata import BWAutomata, Row, Distribution
from bitarray import bitarray
from bitarray.util import ba2int

class ThreeBitRow(Row):

    def __init__(self, width):
        self.width = width
        self.edge = width - 1
        self.vals = bitarray(width)

    def __str__(self):
        return str(self.vals)

    def __repr__(self):
        return self.__str__()

    def set(self, loc, val):
        self.vals[loc] = val

    def gen_vals(self):
        ret_val = self.vals[0:2]
        ret_val.insert(0,self.vals[-1])
        yield ret_val
        for loc in range(1, self.edge):
            yield self.vals[loc-1:loc+2]
        ret_val = self.vals[self.edge-1:self.edge+1]
        ret_val.append(self.vals[0])
        yield ret_val
        return

class ThreeBitAutomata(BWAutomata):

    def get_row(self):
        return ThreeBitRow(self.width)

    def get_pattern(self):
        return bitarray(bin(self.algo)[2:].zfill(8))

    def calculate_it(self, algo_pattern, data):
        loc = ba2int(data)
        return algo_pattern[7-loc]


def verify_pattern():
    row = ThreeBitRow(6)
    for i in range(0, 6, 2):
        row.set(i, 1)
    print(f"row: {row}")
    row_gen = row.gen_vals()
    for i in range(6):
        print(f"{i}: {next(row_gen)}")

    row = ThreeBitRow(6)
    row.set(0, 1)
    row.set(2, 1)
    row.set(3, 1)
    row.set(5, 1)
    print(f"row: {row}")
    row_gen = row.gen_vals()
    for i in range(6):
        print(f"{i}: {next(row_gen)}")


def main():
    parser = argparse.ArgumentParser(description='One dimensional cellular automata that uses three previous cells of colors black and white to determine color')
    parser.add_argument('-w', '--width', type=int, default=1600, help='The width of the window to create')
    parser.add_argument('-i', '--height', type=int, default=1000, help='The height of the window to create')
    parser.add_argument('-a', '--algo', type=int, help="The algorithm number of automata to use (can change with arrow keys while running)", default=30)
    parser.add_argument('-d', '--distribution', type=Distribution, choices=list(Distribution), default=Distribution.single,
                        help="Initial distribution: single point in middle, random, alternating points, clumpy")
    parser.add_argument('-n', '--narrow', type=int, help="Will narrow starting distribution to fraction of width, 10 will be 1/10th of width", default=0)
    args = parser.parse_args()
    automata = ThreeBitAutomata(args.width, args.height, args.algo, args.distribution, args.narrow)
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            verify_pattern()
            return
    automata.run()


if __name__=='__main__':
    main()
