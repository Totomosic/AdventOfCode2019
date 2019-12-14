import sys
sys.path.append("..")
from IntCodeComputer import read_code, IntCodeExecutor

def try_numbers(code_file, result):
    for i in range(100):
        for j in range(100):
            code = read_code(code_file)
            code[1] = i
            code[2] = j
            executor = IntCodeExecutor(code)
            executor.execute()
            if code[0] == result:
                return i, j
    return None
    
code = read_code("IntCode.txt")
executor = IntCodeExecutor(code)
executor.execute()
print("Day 2 - Part 1")
print(code[0])
print(code[0] == 5866714)

noun, verb = try_numbers("IntCode.txt", 19690720)
print("Day 2 - Part 2")
print(noun, verb)
print(noun == 52 and verb == 8)