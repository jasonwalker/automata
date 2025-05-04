from abc import ABC, abstractmethod
import pygame
import sys
from random import randint, seed
from enum import Enum


class Distribution(Enum):
    single = 'single'
    random = 'random'
    alternating = 'alternating'
    clumpy = 'clumpy'

class Row(ABC):

    @abstractmethod
    def gen_vals(self):
        pass

    @abstractmethod
    def set(self, loc, val):
        pass

class Automata(ABC):
    def __init__(self, width, height, colors, algo, distribution, narrowness):
        self.width = width
        self.height = height
        self.colors = colors
        self.height_edge = height - 1
        self.running = True
        self.pause = False
        self.algo = algo
        self.distribution = distribution
        self.narrowness = narrowness
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def pygame_update(self, row_surface):
        self.screen.scroll(0, -1)
        self.screen.blit(row_surface, (0, self.height_edge))
        pygame.display.flip()
        dt = self.clock.tick(120) / 1000

    @abstractmethod
    def get_row(self):
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.algo -= 1
                    print(f"\n\nalgo: {self.algo}\n")
                elif event.key == pygame.K_RIGHT:
                    self.algo += 1
                    print(f"\n\nalgo: {self.algo}\n")
                elif event.key == pygame.K_SPACE:
                    self.pause = not self.pause

    @abstractmethod
    def starting_row(self):
        pass

    @abstractmethod
    def calculate_it(self, algo_pattern, data):
        pass

    @abstractmethod
    def get_pattern(self):
        pass

    def new_row_generator(self, old_row):
        width = old_row.width
        pattern = self.get_pattern()
        while True:
            new_row = self.get_row()
            row_surface = pygame.Surface((width, 1))
            row_vals = old_row.gen_vals()
            for loc, vals in enumerate(row_vals):
                point_color = self.calculate_it(pattern, vals)
                new_row.set(loc, point_color)
                row_surface.set_at((loc, 0), self.colors[point_color])
            old_row = new_row
            yield row_surface


    def run(self):
        pygame.init()
        while self.running:
            row_generator = self.new_row_generator(self.starting_row())
            current_algo = self.algo
            while current_algo == self.algo and self.running:
                self.check_events()
                if not self.pause:
                    row_surface = next(row_generator)
                    self.pygame_update(row_surface)
        pygame.quit()
        sys.exit()

    def get_start_stop(self):
        if self.narrowness != 0:
            print("narrow", self.narrowness)
            return int((self.narrowness-1.0) * self.width / (2.0 * self.narrowness)), int((self.narrowness + 1.0) * self.width / (2.0 *self.narrowness))
        else:
            return 0, self.width


class BWAutomata(Automata):
    def __init__(self, width, height, algo, distribution, narrowness):
        Automata.__init__(self, width, height, [0xffffff, 0x000000], algo, distribution, narrowness)

    def starting_row(self):
        row = self.get_row()
        start_stop = self.get_start_stop()
        if self.distribution == Distribution.single:
            row.set(int(self.width/2),  1)
        elif self.distribution == Distribution.random:
            seed(1)
            for i in range(start_stop[0], start_stop[1]):
                row.set(i, randint(0, 1))
        elif self.distribution == Distribution.alternating:
            for i in range(start_stop[0], start_stop[1], 2):
                row.set(i, 1)
        elif self.distribution == Distribution.clumpy:
            for i in range(start_stop[0] + 3, start_stop[1]-3, 7):
                row.set(i, 0)
                row.set(i+1, 1)
                row.set(i+2, 1)
                row.set(i+5, 1)
                row.set(i+6, 1)
        return row

    @abstractmethod
    def get_row(self):
        pass


class RGBAutomata(Automata):
    def __init__(self, width, height, algo, distribution, narrow_start):
        Automata.__init__(self, width, height, [0xff0000, 0x00ff00, 0x0000ff], algo, distribution, narrow_start)

    def starting_row(self, random=False):
        row = self.get_row()
        start_stop = self.get_start_stop()
        print("start_stop", start_stop)
        if self.distribution == Distribution.single:
            row.set(int(self.width/2),  1)
        elif self.distribution == Distribution.random:
            seed(1)
            for i in range(start_stop[0], start_stop[1]):
                row.set(i, randint(0, 2))
        elif self.distribution == Distribution.alternating:
            for i in range(start_stop[0], start_stop[1], 2):
                row.set(i, 1)
        elif self.distribution == Distribution.clumpy:
            for i in range(start_stop[0] + 3, start_stop[1]-3, 7):
                row.set(i, 1)
                row.set(i+1, 1)
                row.set(i+2, 2)
                row.set(i+5, 1)
                row.set(i+6, 2)
        return row

    @abstractmethod
    def get_row(self):
        pass