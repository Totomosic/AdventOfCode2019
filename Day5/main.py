import sys
sys.path.append("..")
from IntCodeComputer import read_code, IntCodeExecutor, IntCodeInputStream

code = read_code("IntCode.txt")
executor = IntCodeExecutor()
executor.execute(code)