import sys
sys.path.append("..")
from IntCodeComputer import IntCodeExecutor, IntCodeInputStream, IntCodeOutputStream, read_code, STATUS_EXIT

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
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
        self.block_width = int(1280.0 / width)
        self.block_height = int(720.0 / height)

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

class Game:
    def __init__(self, code, board):
        self.executor = IntCodeExecutor(code, IntCodeInputStream(), IntCodeOutputStream())
        self.board = board
        self.score = 0

        self.ball = np.array([0,0])
        self.player = np.array([0,0])

    def create_board(self):
        self.executor.clear_streams()
        self.executor.execute()
        results = []
        while not self.executor.stdout.empty():
            results.append(self.executor.stdout.read())
        self.process_results(results)

    def process_results(self, results):
        for i in range(0, len(results), 3):
            x = results[i + 0]
            y = results[i + 1]
            value = results[i + 2]
            if not (x == -1 and y == 0):
                self.board.set_cell(x, y, value)
                if value == 4:
                    self.ball = np.array([x,y])
                elif value == 3:
                    self.player = np.array([x,y])
            else:
                self.score = value

    def run(self):
        clock = pygame.time.Clock()
        self.create_board()
        self.executor.clear_streams()
        joystick = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # AI
            dx = self.ball[0] - self.player[0]
            joystick = 1 if dx > 0 else (-1 if dx < 0 else 0)

            self.executor.stdin.write(joystick)
            status = self.executor.execute()
            results = []
            while not self.executor.stdout.empty():
                results.append(self.executor.stdout.read())
            self.process_results(results)
            if status == STATUS_EXIT:
                break

            display.fill((0,0,0))
            self.board.draw(display)
            pygame.display.update()

code = read_code("IntCode.txt")
board = GameBoard(42, 23)
game = Game(code, board)
game.create_board()

count = 0
for cell in board.grid.flatten():
    if cell == 2:
        count += 1
print("Day 13 - Part 1")
print(count)
print(count == 233)

pygame.init()
display = pygame.display.set_mode((1280,720))
pygame.display.set_caption("IntCode Breakout")

code = read_code("IntCode.txt")
code[0] = 2
board = GameBoard(42, 23)
game = Game(code, board)
game.run()
print("Day 13 - Part 2")
print(game.score)
print(game.score == 11991)