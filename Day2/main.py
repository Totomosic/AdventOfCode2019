import sys
sys.path.append("..")
from IntCodeComputer import read_code, run_code

def try_numbers(code_file, result):
    for i in range(100):
        for j in range(100):
            code = read_code(code_file)
            code[1] = i
            code[2] = j
            run_code(code)
            if code[0] == result:
                return i, j
    return None
    
code = read_code("IntCode.txt")
run_code(code)
print(code)

noun, verb = try_numbers("IntCode.txt", 19690720)
print(noun, verb)