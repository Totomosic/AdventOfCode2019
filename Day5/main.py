import sys
sys.path.append("..")
from IntCodeComputer import read_code, IntCodeExecutor, IntCodeInputStream, IntCodeOutputStream

code = read_code("IntCode.txt")
executor = IntCodeExecutor(code, stdout=IntCodeOutputStream())
executor.stdin.write(1)
executor.execute()
print("Day 5 - Part 1")
value = None
while not executor.stdout.empty():
    value = executor.stdout.read()
    print(value)
print(value == 14155342)

code = read_code("IntCode.txt")
executor = IntCodeExecutor(code, IntCodeInputStream(), IntCodeOutputStream())
executor.stdin.write(5)
executor.execute()
print("Day 5 - Part 2")
value = None
while not executor.stdout.empty():
    value = executor.stdout.read()
    print(value)
print(value == 8684145)