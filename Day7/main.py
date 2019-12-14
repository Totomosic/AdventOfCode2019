import sys
sys.path.append("..")
from IntCodeComputer import read_code, IntCodeExecutor, IntCodeInputStream, IntCodeOutputStream
import itertools

CODE_FILE = "IntCode.txt"

AMPLIFIER_COUNT = 5
phase_settings = list(itertools.permutations(range(AMPLIFIER_COUNT)))
max_value = 0
best_combination = None

for combination in phase_settings:
    output = 0
    index = 0
    executors = [IntCodeExecutor(read_code(CODE_FILE), IntCodeInputStream(), IntCodeOutputStream()) for i in range(AMPLIFIER_COUNT)]
    for setting, executor in zip(combination, executors):
        executor.reset()
        executor.clear_streams()
        executor.stdin.write(setting)
        executor.stdin.write(output)
        executor.execute()
        output = executor.stdout.read()
        index += 1
    if output > max_value:
        max_value = output
        best_combination = combination

print("Day 7 - Part 1")
print(max_value, best_combination)
print(max_value == 118936)

phase_settings = list(itertools.permutations(range(5, 10)))
max_value = 0
best_combination = None

for combination in phase_settings:
    executor.clear_streams()
    output = 0
    executors = [IntCodeExecutor(read_code(CODE_FILE), IntCodeInputStream(), IntCodeOutputStream()) for i in range(AMPLIFIER_COUNT)]
    for setting, executor in zip(combination, executors):
        executor.stdin.write(setting)
        executor.stdin.write(output)
        executor.execute({ 4: lambda: True })
        output = executor.stdout.read()
    exited = False
    while not exited:
        for executor in executors:
            executor.stdin.write(output)
            exited = executor.execute({ 4: lambda: True })
            if exited:
                break
            output = executor.stdout.read()
    if output > max_value:
        max_value = output
        best_combination = combination

print("Day 7 - Part 2")
print(max_value, best_combination)
print(max_value == 57660948)