#!/usr/bin/python3

##
##  automata that uses three cells above, left, center and right, each with values 0,1 or 2
##

import numpy as np
import sys
from lib.automata import RGBAutomata, Row

class Base3Row(Row):
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
        return Base3Row(self.width)

    def get_pattern(self):
        return np.base_repr(self.algo, 3).zfill(27)

    def calculate_it(self, algo_pattern, data):
        as_string = ''.join(map(str, data))
        print("as_string", as_string)
        loc = int(as_string, 3)
        return int(algo_pattern[26-loc])


def verify_pattern():
    row = Base3Row(6)
    for i in range(0, 6, 2):
        row.set(i, 1)
    print(f"row: {row}")
    row_gen = row.gen_vals()
    for i in range(6):
        print(f"{i}: {next(row_gen)}")

    row = Base3Row(6)
    row.set(0, 1)
    row.set(2, 2)
    row.set(3, 1)
    row.set(5, 2)
    print(f"row: {row}")
    row_gen = row.gen_vals()
    for i in range(6):
        print(f"{i}: {next(row_gen)}")


def main():
    algo = int(sys.argv[1]) if len(sys.argv) > 1 else 197252530603
    automata = ThreeCellRGBAutomata(1600, 1000, algo, 'single')
    automata.run()


if __name__=='__main__':
    main()
