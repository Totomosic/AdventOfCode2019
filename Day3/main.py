import numpy as np
import math

DIRECTIONS = {
    'R' : np.array([1, 0]),
    'L' : np.array([-1, 0]),
    'U' : np.array([0, 1]),
    'D' : np.array([0, -1])
}

def segment_intersection(l0, l1):
    p0 = l0[0]
    d0 = l0[1] - l0[0]
    p1 = l1[0]
    d1 = l1[1] - l1[0]
    dot = np.dot(d0, d1)
    if (d0[0] == 0 and d1[0] == 0) or (d0[1] == 0 and d1[1] == 0):
        return None
    if d0[1] == 0:
        x0, x1 = p0[0], p0[0] + d0[0]
        x = p1[0]
        y0, y1 = p1[1], p1[1] + d1[1]
        y = p0[1]
        if not (x >= min([x0, x1]) and x <= max([x0, x1]) and y >= min([y0, y1]) and y <= max([y0, y1])):
            return None
        return np.array([p1[0], p0[1]])
    else:
        x0, x1 = p1[0], p1[0] + d1[0]
        x = p0[0]
        y0, y1 = p0[1], p0[1] + d0[1]
        y = p1[1]
        if not (x >= min([x0, x1]) and x <= max([x0, x1]) and y >= min([y0, y1]) and y <= max([y0, y1])):
            return None
        return np.array([p0[0], p1[1]])

def is_point_on_line(p0, p1, point):
    d0 = p1 - p0
    d1 = point - p0
    if not ((d0[0] == d1[0] and d0[0] == 0) or (d0[1] == d1[1] and d0[1] == 0)):
        return False
    maxX = p1[0] - p0[0]
    dx = point[0] - p0[0]
    maxY = p1[1] - p0[1]
    dy = point[1] - p0[1]
    if abs(dx) <= abs(maxX) and abs(dx) > 0:
        return True
    if abs(dy) <= abs(maxY) and abs(dy) > 0:
        return True
    return False

class WireNetwork:
    def __init__(self, instructions):
        self.positions = []
        self._create_path(instructions)

    def find_intersections(self, network):
        result = []
        for i in range(1, len(self.positions)):
            p0 = self.positions[i - 1]
            p1 = self.positions[i]
            for j in range(1, len(network.positions)):
                other_p0 = network.positions[j - 1]
                other_p1 = network.positions[j]
                intersection = segment_intersection((p0, p1), (other_p0, other_p1))
                if intersection is not None:
                    result.append(intersection)
        return result

    def find_steps_to_point(self, point):
        steps = 0
        for i in range(1, len(self.positions)):
            p0 = self.positions[i - 1]
            p1 = self.positions[i]
            if is_point_on_line(p0, p1, point):
                distance = round(np.linalg.norm(point - p0))
                steps += distance
                return int(steps)
            steps += round(np.linalg.norm(p1 - p0))
        return None

    def _create_path(self, instructions):
        current_position = np.array([0, 0])
        self.positions.append(np.array(current_position))
        for instruction in instructions:
            direction = DIRECTIONS[instruction[0]]
            amount = int(instruction[1:])
            current_position += direction * amount
            self.positions.append(np.array(current_position))

def find_intersections(networks):
    result = []
    for index in range(len(networks)):
        n0 = networks[index]
        for other_index in range(index):
            n1 = networks[other_index]
            intersections = n0.find_intersections(n1)
            result.append({ "networks" : (n0, n1), "points" : intersections })
    return result

def find_min_distance_intersection(intersections):
    min_distance = math.inf
    for network_pair in intersections:
        for point in network_pair["points"]:
            distance = abs(point[0]) + abs(point[1])
            if distance < min_distance and distance != 0:
                min_distance = distance
    return min_distance

def find_intersection_steps(intersections):
    result = []
    for network_pair in intersections:
        for point in network_pair["points"]:
            if point.any():
                steps = 0
                for network in network_pair["networks"]:
                    s = network.find_steps_to_point(point)
                    if s is not None:
                        steps += s
                result.append(steps)
    return result

def read_input(file):
    with open(file, "r") as f:
        lines = f.readlines()
        result = []
        for line in lines:
            line = line.replace('\r', '').replace('\n', '').replace('\t', '')
            result.append(line.split(','))
        return result

instruction_sets = read_input("input.txt")
networks = []
for instructions in instruction_sets:
    networks.append(WireNetwork(instructions))

intersections = find_intersections(networks)
distance = find_min_distance_intersection(intersections)
print("Day 3 - Part 1")
print(distance)
print(distance == 221)

steps = find_intersection_steps(intersections)
result = min(steps)
print("Day 3 - Part 2")
print(result)
print(result == 18542)