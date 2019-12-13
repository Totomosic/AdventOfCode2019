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