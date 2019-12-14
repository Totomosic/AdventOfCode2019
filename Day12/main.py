import numpy as np
from math import gcd

def read_input(file):
    with open(file, "r") as f:
        result = []
        velocities = []
        for line in f.readlines():
            line = line.replace('\n','').replace('\r','').replace('<','').replace('>','').replace(' ','')
            parts = line.split(',')
            x = int(parts[0][parts[0].index('=') + 1:])
            y = int(parts[1][parts[1].index('=') + 1:])
            z = int(parts[2][parts[2].index('=') + 1:])
            result.append(np.array([x,y,z]))
            velocities.append(np.array([0,0,0]))
        return result, velocities

def simulate_axis(positions, velocities, axis):
    for position, velocity in zip(positions, velocities):
        d = 0
        for other_p, other_v in zip(positions, velocities):
            if other_p is position:
                continue
            delta = other_p - position
            if delta[axis] > 0:
                d += 1
            elif delta[axis] < 0:
                d -= 1
        velocity[axis] += d
    for position, velocity in zip(positions, velocities):
        position[axis] += velocity[axis]

def simulate(positions, velocities):
    simulate_axis(positions, velocities, 0)
    simulate_axis(positions, velocities, 1)
    simulate_axis(positions, velocities, 2)

def find_cycle_length(positions, velocities, axis):
    steps = 0
    originals = [p[axis] for p in positions]
    while True:
        simulate_axis(positions, velocities, axis)
        steps += 1
        done = True
        # Check that velocity and position are the original
        for velocity, index in zip(velocities, range(len(velocities))):
            if velocity[axis] != 0 or positions[index][axis] != originals[index]:
                done = False
                break
        if done:
            break
    return steps

def find_lcm(values):
    lcm = values[0]
    for i in values[1:]:
        lcm = int(lcm * i / gcd(lcm, i))
    return lcm

def calculate_kinetic_energy(velocity):
    return abs(velocity[0]) + abs(velocity[1]) + abs(velocity[2])

def calculate_potential_energy(position):
    return abs(position[0]) + abs(position[1]) + abs(position[2])

def calculate_total_energy(position, velocity):
    return calculate_potential_energy(position) * calculate_kinetic_energy(velocity)

def calculate_sytem_energy(positions, velocities):
    energy = 0
    for position, velocity in zip(positions, velocities):
        energy += calculate_total_energy(position, velocity)
    return energy

positions, velocities = read_input("input.txt")
for i in range(1000):
    simulate(positions, velocities)

energy = calculate_sytem_energy(positions,velocities)
print("Day 12 - Part 1")
print(energy)
print(energy == 7077)

positions, velocities = read_input("input.txt")
x = find_cycle_length(positions, velocities, 0)
y = find_cycle_length(positions, velocities, 1)
z = find_cycle_length(positions, velocities, 2)
total = find_lcm([x, y, z])
print("Day 12 - Part 2")
print(total)
print(total == 402951477454512)