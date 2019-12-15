import sys
sys.path.append("..")
from IntCodeComputer import read_code, IntCodeExecutor, IntCodeInputStream, IntCodeOutputStream, STATUS_EXIT
import itertools

CODE_FILE = "IntCode.txt"

AMPLIFIER_COUNT = 5
phase_settings = list(itertools.permutations(range(AMPLIFIER_COUNT)))
max_value = 0
best_combination = None

for combination in phase_settings:
    executors = [IntCodeExecutor(read_code(CODE_FILE), IntCodeInputStream(), IntCodeOutputStream()) for i in range(AMPLIFIER_COUNT)]

    for i in range(len(executors) - 1):
        executors[i].stdin.write(combination[i])
        executors[i].stdout = executors[i + 1].stdin
    executors[-1].stdin.write(combination[-1])

    executors[0].stdin.write(0)
    for executor in executors:
        executor.execute()

    output = executors[-1].stdout.read()
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
    executors = [IntCodeExecutor(read_code(CODE_FILE), IntCodeInputStream(), IntCodeOutputStream()) for i in range(AMPLIFIER_COUNT)]
    # Connect executors together in loop
    for i in range(len(executors)):
        executors[i - 1].stdin.write(combination[i - 1])
        executors[i - 1].stdout = executors[i].stdin
    executors[0].stdin.write(0)
    
    status = None
    while status != STATUS_EXIT:
        for executor in executors:
            status = executor.execute()
    
    output = executors[-1].stdout.read()
    if output > max_value:
        max_value = output
        best_combination = combination

print("Day 7 - Part 2")
print(max_value, best_combination)
print(max_value == 57660948)