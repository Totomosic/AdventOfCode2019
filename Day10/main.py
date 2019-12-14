import numpy as np
import math

def read_map(file):
    with open(file, "r") as f:
        result = []
        for line in f.readlines():
            line = line.replace('\n','').replace('\r','')
            result.append(list(map(lambda c: True if c == '#' else False, list(line))))
        return result

def is_asteroid(asteroids, x, y):
    return asteroids[y][x]

def calculate_gcd(a, b):
    divisor = max([abs(a), abs(b)])
    while True:
        if a % divisor == 0 and b % divisor == 0:
            return divisor
        divisor -= 1

def calculate_integer_direction(point1, point2):
    direction = np.array(point2) - np.array(point1)
    divisor = calculate_gcd(direction[0], direction[1])
    return int(direction[0] / divisor), int(direction[1] / divisor)

def calculate_visible_asteroids(asteroids, x, y):
    width = len(asteroids[0])
    height = len(asteroids)
    visible = []
    for i in range(width):
        for j in range(height):
            if i == x and j == y:
                continue
            if is_asteroid(asteroids, i, j):                
                direction = calculate_integer_direction((x, y), (i, j))
                position = (x + direction[0], y + direction[1])
                valid = True
                while not (position[0] == i and position[1] == j):
                    if is_asteroid(asteroids, position[0], position[1]):
                        valid = False
                        break
                    position = (position[0] + direction[0], position[1] + direction[1])
                if valid:
                    visible.append((i, j))
    return visible

def get_asteroid_angle(asteroid, reference):
    direction = np.array(asteroid) - np.array(reference)
    direction = np.array([direction[1] * -1, direction[0]])
    angle = math.atan2(direction[1], direction[0])
    
    if angle < 0:
        angle = 2 * math.pi + angle
    return angle

def vaporize(asteroids, x, y):
    total = len(asteroids) * len(asteroids[0])
    order = []
    while True:
        visible = calculate_visible_asteroids(asteroids, x, y)
        if len(visible) == 0:
            break
        visible.sort(key=lambda asteroid: get_asteroid_angle(asteroid, (x,y)), reverse=False)
        for a in visible:
            order.append(a)
            asteroids[a[1]][a[0]] = False
        break
    return order

asteroids = read_map("map.txt")
width = len(asteroids[0])
height = len(asteroids)

x = None
y = None
max_visible = 0

for i in range(width):
    for j in range(height):
        if is_asteroid(asteroids, i, j):
            nvisible = len(calculate_visible_asteroids(asteroids, i, j))
            if nvisible > max_visible:
                max_visible = nvisible
                x = i
                y = j

print(x, y, max_visible)
order = vaporize(asteroids, x, y)
print(order[199])