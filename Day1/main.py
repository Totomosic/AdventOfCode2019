import sys
import os

input_file = "input.txt"

with open(input_file, "r") as f:
    data = f.read()
    data = data.replace(' ', '').replace('\r', '')
    data = data.split('\n')    

numbers = []
for d in data:
    numbers.append(int(d))

def calculate_fuel(mass):
    return int(float(mass) / 3.0) - 2

total = 0
for mass in numbers:
    total += calculate_fuel(mass)
print("Day 1 - Part 1")
print(total)
print(total == 3358992)

total = 0
for mass in numbers:
    fuel_mass = calculate_fuel(mass)
    while fuel_mass > 0:
        total += fuel_mass
        fuel_mass = calculate_fuel(fuel_mass)
print("Day 1 - Part 2")
print(total)
print(total == 5035632)