import sys
sys.path.append("..")
from IntCodeComputer import read_code, run_code

code = read_code("IntCode.txt")
run_code(code)