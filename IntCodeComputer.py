# ============================================================================================================
# UTILITIES
# ============================================================================================================

EXIT_STATUS = -1
TRUE = 1
FALSE = 0

def parse_opcode(opcode):
    if opcode < 100:
        return (opcode, [])
    string = str(opcode)
    opcode = int(string[-2:])
    param_modes = []
    for i in reversed(range(len(string) - 2)):
        param_modes.append(int(string[i]))
    return (opcode, param_modes)

def read_code(file, memory_padding=1000):
    with open(file, "r") as f:
        string_codes = f.read().split(',')
        result = []
        for code in string_codes:
            result.append(int(code))
        result += [0 for i in range(memory_padding)]
        return result

# ============================================================================================================
# STREAM WRAPPERS
# ============================================================================================================

class IntCodeStdin:
    def __init__(self, prompt="> "):
        self.prompt = prompt
        self.buffer = []

    def read(self):
        if len(self.buffer) > 0:
            return self.buffer.pop(0)
        return input(self.prompt)

    def clear(self):
        self.buffer = []

    def write(self, value):
        self.buffer.append(value)

class IntCodeInputStream:
    def __init__(self):
        self.buffer = []

    def read(self):
        if len(self.buffer) > 0:
            return self.buffer.pop(0)
        raise IndexError("Input stream ran out of data")

    def clear(self):
        self.buffer = []

    def write(self, value):
        self.buffer.append(value)

class IntCodeStdout:
    def __init__(self):
        pass

    def write(self, value):
        print(value)

    def clear(self):
        pass

class IntCodeOutputStream:
    def __init__(self):
        self.buffer = []

    def write(self, value):
        self.buffer.append(value)

    def clear(self):
        self.buffer = []

    def read(self):
        if len(self.buffer) > 0:
            return self.buffer.pop(0)
        raise IndexError("Output stream ran out of data")

# ============================================================================================================
# EXECUTOR
# ============================================================================================================

class IntCodeExecutor:
    def __init__(self, stdin=IntCodeStdin(), stdout=IntCodeStdout()):
        self.stdin = stdin
        self.stdout = stdout

        self.instruction_pointer = 0
        self.relative_base = 0

        self.parameter_mode_map = {
            0 : self.parammode_0,
            1 : self.parammode_1,
            2 : self.parammode_2
        }

        self.opcode_map = {
            1 : self.opcode_1,
            2 : self.opcode_2,
            3 : self.opcode_3,
            4 : self.opcode_4,
            5 : self.opcode_5,
            6 : self.opcode_6,
            7 : self.opcode_7,
            8 : self.opcode_8,
            9 : self.opcode_9,
            99 : self.opcode_99
        }

    def reset(self):
        self.relative_base = 0
        self.instruction_pointer = 0

    def clear_streams(self):
        self.stdin.clear()
        self.stdout.clear()

    def execute(self, code, callback_map={}):
        while self.instruction_pointer < len(code):
            full_opcode = code[self.instruction_pointer]
            opcode, parameter_modes = parse_opcode(full_opcode)
            result = self.opcode_map[opcode](code, self.instruction_pointer, parameter_modes)
            self.instruction_pointer = result
            if opcode in callback_map:
                if callback_map[opcode]():
                    return False
            if result == EXIT_STATUS:
                return True    
        return True        

    def get_parameter_value(self, code, baseIndex, index, parameter_modes, is_output=False):
        mode = 0
        if index - 1 < len(parameter_modes):
            mode = parameter_modes[index - 1]
        return self.parameter_mode_map[mode](code, index + baseIndex, is_output)

    # ============================================================================================================
    # PARAMETER MODES
    # ============================================================================================================

    # Position Mode
    def parammode_0(self, code, current_index, is_output):
        index = code[current_index]
        if is_output:
            return index
        return code[index]

    # Immediate Mode
    def parammode_1(self, code, current_index, is_output):
        index = current_index
        if is_output:
            return index
        return code[index]

    # Relative Mode
    def parammode_2(self, code, current_index, is_output):
        index = code[current_index] + self.relative_base
        if is_output:
            return index
        return code[index]

    # ============================================================================================================
    # OPCODES
    # ============================================================================================================

    # Add
    def opcode_1(self, code, current_index, parameter_modes):
        output_index = self.get_parameter_value(code, current_index, 3, parameter_modes, is_output=True)
        code[output_index] = self.get_parameter_value(code, current_index, 1, parameter_modes) + self.get_parameter_value(code, current_index, 2, parameter_modes)
        return current_index + 4

    # Multiply
    def opcode_2(self, code, current_index, parameter_modes):
        output_index = self.get_parameter_value(code, current_index, 3, parameter_modes, is_output=True)
        code[output_index] = self.get_parameter_value(code, current_index, 1, parameter_modes) * self.get_parameter_value(code, current_index, 2, parameter_modes)
        return current_index + 4

    # Input
    def opcode_3(self, code, current_index, parameter_modes):
        output_index = self.get_parameter_value(code, current_index, 1, parameter_modes, is_output=True)
        code[output_index] = int(self.stdin.read())
        return current_index + 2

    # Output
    def opcode_4(self, code, current_index, parameter_modes):
        value = self.get_parameter_value(code, current_index, 1, parameter_modes)
        self.stdout.write(value)
        return current_index + 2

    # Jump if true
    def opcode_5(self, code, current_index, parameter_modes):
        value = self.get_parameter_value(code, current_index, 1, parameter_modes)
        if value != FALSE:
            return self.get_parameter_value(code, current_index, 2, parameter_modes)
        return current_index + 3

    # Jump if false
    def opcode_6(self, code, current_index, parameter_modes):
        value = self.get_parameter_value(code, current_index, 1, parameter_modes)
        if value == FALSE:
            return self.get_parameter_value(code, current_index, 2, parameter_modes)
        return current_index + 3

    # Less than
    def opcode_7(self, code, current_index, parameter_modes):
        output_index = self.get_parameter_value(code, current_index, 3, parameter_modes, is_output=True)
        if self.get_parameter_value(code, current_index, 1, parameter_modes) < self.get_parameter_value(code, current_index, 2, parameter_modes):
            code[output_index] = TRUE
        else:
            code[output_index] = FALSE
        return current_index + 4

    # Equals
    def opcode_8(self, code, current_index, parameter_modes):
        output_index = self.get_parameter_value(code, current_index, 3, parameter_modes, is_output=True)
        if self.get_parameter_value(code, current_index, 1, parameter_modes) == self.get_parameter_value(code, current_index, 2, parameter_modes):
            code[output_index] = TRUE
        else:
            code[output_index] = FALSE
        return current_index + 4

    # Relative base shift
    def opcode_9(self, code, current_index, parameter_modes):
        value = self.get_parameter_value(code, current_index, 1, parameter_modes)
        self.relative_base += value
        return current_index + 2

    # Exit
    def opcode_99(self, code, current_index, parameter_modes):
        return EXIT_STATUS