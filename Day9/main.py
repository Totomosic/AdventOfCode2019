import sys
sys.path.append("..")
from IntCodeComputer import read_code, IntCodeExecutor, IntCodeInputStream, IntCodeOutputStream

code = read_code("IntCode.txt")
executor = IntCodeExecutor(code, IntCodeInputStream(), IntCodeOutputStream())
executor.stdin.write(1)
executor.execute()
result = executor.stdout.read()
print("Day 9 - Part 1")
print(result)
print(result == 3497884671)

code = read_code("IntCode.txt")
executor = IntCodeExecutor(code, IntCodeInputStream(), IntCodeOutputStream())
executor.stdin.write(2)
executor.execute()
result = executor.stdout.read()
print("Day 9 - Part 2")
print(result)
print(result == 46470)