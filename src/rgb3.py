#!/usr/bin/python3

##
##  automata that uses three cells above, left, center and right, each with values 0, 1 or 2
##

import argparse
import numpy as np
from lib.automata import RGBAutomata, Row, Distribution

class Base3Row3Cells(Row):
    def __init__(self, width):
        self.edge = width - 1
        self.vals = [0] * width
        self.width = width

    def __str__(self):
        return str(self.vals)

    def __repr__(self):
        return self.__str__()

    def set(self, loc, val):
        self.vals[loc] = val

    def gen_vals(self):
        yield [self.vals[self.edge], self.vals[0], self.vals[1]]
        for loc in range(1, self.edge):
            yield [self.vals[loc-1], self.vals[loc], self.vals[loc+1]]
        yield [self.vals[self.edge-1], self.vals[self.edge], self.vals[0]]
        return


class ThreeCellRGBAutomata(RGBAutomata):
    def get_row(self):
        return Base3Row3Cells(self.width)

    def get_pattern(self):
        return np.base_repr(self.algo, 3).zfill(27)

    def calculate_it(self, algo_pattern, data):
        as_string = ''.join(map(str, data))
        loc = int(as_string, 3)
        return int(algo_pattern[26-loc])


def verify_pattern():
    row = Base3Row3Cells(6)
    for i in range(0, 6, 2):
        row.set(i, 1)
    print(f"row: {row}")
    row_gen = row.gen_vals()
    for i in range(6):
        print(f"{i}: {next(row_gen)}")

    row = Base3Row3Cells(6)
    row.set(0, 1)
    row.set(2, 2)
    row.set(3, 1)
    row.set(5, 2)
    print(f"row: {row}")
    row_gen = row.gen_vals()
    for i in range(6):
        print(f"{i}: {next(row_gen)}")


def main():
    parser = argparse.ArgumentParser(description='One dimensional cellular automata that uses three previous cells of colors red, green and blue to determine color')
    parser.add_argument('-w', '--width', type=int, default=1600, help='The width of the window to create')
    parser.add_argument('-i', '--height', type=int, default=1000, help='The height of the window to create')
    parser.add_argument('-a', '--algo', type=int, help="The algorithm number of automata to use (can change with arrow keys while running)", default=197252530603)
    parser.add_argument('-d', '--distribution', type=Distribution, choices=list(Distribution), default=Distribution.single,
                        help="Initial distribution: single point in middle, random, alternating points, clumpy")
    parser.add_argument('-n', '--narrow', type=int, help="Will narrow starting distribution to fraction of width, 10 will be 1/10th of width", default=0)
    args = parser.parse_args()

    automata = ThreeCellRGBAutomata(args.width, args.height, args.algo, args.distribution, args.narrow)
    automata.run()


if __name__=='__main__':
    main()
