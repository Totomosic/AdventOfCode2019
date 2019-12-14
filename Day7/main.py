import sys
sys.path.append("..")
from IntCodeComputer import read_code, IntCodeExecutor, IntCodeInputStream, IntCodeOutputStream
import itertools

AMPLIFIER_COUNT = 5
phase_settings = list(itertools.permutations(range(AMPLIFIER_COUNT)))

CODE_FILE = "IntCode.txt"

executor = IntCodeExecutor()
executor.stdin = IntCodeInputStream()
executor.stdout = IntCodeOutputStream()

max_value = 0
best_combination = None

for combination in phase_settings:
    output = 0
    index = 0
    codes = [read_code(CODE_FILE) for i in range(AMPLIFIER_COUNT)]
    for setting in combination:
        executor.reset()
        executor.clear_streams()
        executor.stdin.write(setting)
        executor.stdin.write(output)
        code = codes[index]
        executor.execute(code)
        output = executor.stdout.read()
        index += 1
    if output > max_value:
        max_value = output
        best_combination = combination

print(max_value, best_combination)

phase_settings = list(itertools.permutations(range(5, 10)))
executor.reset()

max_value = 0
best_combination = None

for combination in phase_settings:
    executor.clear_streams()
    output = 0
    codes = [read_code(CODE_FILE) for i in range(AMPLIFIER_COUNT)]
    executors = [IntCodeExecutor(IntCodeInputStream(), IntCodeOutputStream()) for i in range(AMPLIFIER_COUNT)]
    for setting, code, executor in zip(combination, codes, executors):
        executor.stdin.write(setting)
        executor.stdin.write(output)
        executor.execute(code, { 4: lambda: True })
        output = executor.stdout.read()
    exited = False
    while not exited:
        for amplifier, executor in zip(codes, executors):
            executor.stdin.write(output)
            exited = executor.execute(amplifier, { 4: lambda: True })
            if exited:
                break
            output = executor.stdout.read()
    if output > max_value:
        max_value = output
        best_combination = combination

print(max_value, best_combination)