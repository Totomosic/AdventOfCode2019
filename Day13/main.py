import sys
sys.path.append("..")
from IntCodeComputer import IntCodeExecutor, IntCodeInputStream, IntCodeOutputStream, read_code

import pygame
import numpy as np

COLOR_MAP = {
    0 : None,
    1 : (255,255,255),
    2 : (100,100,100),
    3 : (0,255,0),
    4 : (255,0,0)
}

class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_width = 10
        self.block_height = 10

        self.grid = np.zeros((self.width, self.height), dtype=int)

    def get_cell(self, x, y):
        return self.grid[int(x)][int(y)]

    def set_cell(self, x, y, value):
        self.grid[int(x)][int(y)] = value

    def draw(self, display):
        for i in range(self.width):
            for j in range(self.height):
                mode = self.get_cell(i, j)
                color = COLOR_MAP[mode]
                if color is not None:
                    pygame.draw.rect(display, color, (i * self.block_width, j * self.block_height, self.block_width, self.block_height))

pygame.init()
display = pygame.display.set_mode((1280,720))

game = GameBoard(128, 72)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    display.fill((0,0,0))
    game.draw(display)
    pygame.display.update()