import sys
sys.path.append("..")
from IntCodeComputer import read_code, IntCodeExecutor, IntCodeInputStream, IntCodeOutputStream

import numpy as np
from PIL import Image

LEFT = 0
RIGHT = 1

class PaintingPanel:
    def __init__(self, size):
        self.size = np.array(size)
        self.values = np.zeros(self.size, dtype=np.int)
        self.painted = []

    def get_value(self, x, y):
        return self.values[int(x)][int(y)]
    
    def set_value(self, x, y, value):
        self.values[int(x)][int(y)] = value
        v = (x,y)
        if v not in self.painted:
            self.painted.append(v)

    def set_middle(self, value):
        self.set_value(self.size[0] / 2, self.size[1] / 2, value)

class PaintingRobot:
    def __init__(self, code):
        self.executor = IntCodeExecutor(code)
        self.executor.stdin = IntCodeInputStream()
        self.executor.stdout = IntCodeOutputStream()
        self.position = None
        self.direction = None

    def change_direction(self, direction):
        multiplier = -1 if direction == LEFT else 1
        if self.direction[0] == 0:
            self.direction[0] = self.direction[1] * multiplier
            self.direction[1] = 0
        else:
            self.direction[1] = self.direction[0] * -multiplier
            self.direction[0] = 0

    def paint(self, panel):
        self.executor.reset()
        self.executor.clear_streams()
        self.position = (panel.size / 2).astype(np.int)
        self.direction = np.array([0, 1], dtype=np.int)
        while True:
            current_value = panel.get_value(self.position[0], self.position[1])
            self.executor.stdin.write(current_value)
            exited = self.executor.execute({ 4: lambda: True })
            if exited:
                break
            new_value = self.executor.stdout.read()
            panel.set_value(self.position[0], self.position[1], new_value)
            exited = self.executor.execute({ 4: lambda: True })
            if exited:
                break
            direction = self.executor.stdout.read()
            self.change_direction(direction)
            self.position += self.direction

code = read_code("IntCode.txt")
panel = PaintingPanel((100,100))
robot = PaintingRobot(code)
robot.paint(panel)
result = len(panel.painted)
print("Day 11 - Part 1")
print(result)
print(result == 1934)

code = read_code("IntCode.txt")
panel = PaintingPanel((100,100))
panel.set_middle(1)
robot = PaintingRobot(code)
robot.paint(panel)
print("Day 11 - Part 2")
print("See Image")
image = Image.fromarray(panel.values * 255)
image.show()
print(True)