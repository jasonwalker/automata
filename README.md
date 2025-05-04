# Automata

An implementation of 1-dimensional cellular automata _https://en.wikipedia.org/wiki/Elementary_cellular_automaton_ with some variations

## Quick Start
(_These are written in Python and it is helpful to use 'uv'_)
uv run src/bw2.py

## Naming Conventions
The scripts are named as follows:

The first letter:

bw - uses two colors for cells - black and white
rgb - uses three colors for cells, red, green and blue

The number - the number of previous cells to determine the current cell
2 - uses the cell to the left and right, but not center
3 - uses left, center and right previous cells
4 - uses 2 left and 2 right cells, but not center cell




