# Automata

An implementation of 1-dimensional cellular automata _https://en.wikipedia.org/wiki/Elementary_cellular_automaton_ with some variations

## Quick Start
(_These are written in Python and it is helpful to use 'uv'_)

uv run src/bw2.py

uv run src/rgb3.py

uv run src/bw2.py -r 6 -d random -n 10

uv run src/bw3.py -r 30 -d single 

uv run src/rgb3.py -d clumpy -n 10

## Controls
While the automata is scrolling, you can:

**left arrow** go to previous rule

**right arrow** go to next rule

**space bar** pause the scrolling


## Options

**-w**: Width of window

**-h**: Height of window

**-r**: rule number that follows the standard naming convention (Wolfram code)

**-d**: initial distribution of cell colors

**-n**: if distibution is random, alternating or clump (not single), how wide to make the distribution as a fraction 10 would be 1/10th total width


## Naming Conventions

The scripts are named as follows:

The first letter:

**bw** - uses two colors for cells - black and white

**rgb** - uses three colors for cells, red, green and blue

The number - the number of previous cells to determine the current cell

**2** - uses the cell to the left and right, but not center

**3** - uses left, center and right previous cells

**4** - uses 2 left and 2 right cells, but not center cell






