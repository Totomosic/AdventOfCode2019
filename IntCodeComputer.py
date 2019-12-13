# ============================================================================================================
# UTILITIES
# ============================================================================================================

def get_parameter_value(code, baseIndex, index, parameter_modes, is_output=False):
    mode = 0
    if index - 1 < len(parameter_modes):
        mode = parameter_modes[index - 1]
    if is_output:
        mode = 1
    return PARAMETER_MODE_MAP[mode](code, index + baseIndex)

def parse_opcode(opcode):
    if opcode < 100:
        return (opcode, [])
    string = str(opcode)
    opcode = int(string[-2:])
    param_modes = []
    for i in reversed(range(len(string) - 2)):
        param_modes.append(int(string[i]))
    return (opcode, param_modes)

# ============================================================================================================
# PARAMETER MODES
# ============================================================================================================

# Position Mode
def parammode_0(code, current_index):
    return code[code[current_index]]

# Immediate Mode
def parammode_1(code, current_index):
    return code[current_index]

# ============================================================================================================
# OPCODES
# ============================================================================================================

EXIT_STATUS = -1
TRUE = 1
FALSE = 0

# Add
def opcode_1(code, current_index, parameter_modes):
    output_index = get_parameter_value(code, current_index, 3, parameter_modes, is_output=True)
    code[output_index] = get_parameter_value(code, current_index, 1, parameter_modes) + get_parameter_value(code, current_index, 2, parameter_modes)
    return current_index + 4

# Multiply
def opcode_2(code, current_index, parameter_modes):
    output_index = get_parameter_value(code, current_index, 3, parameter_modes, is_output=True)
    code[output_index] = get_parameter_value(code, current_index, 1, parameter_modes) * get_parameter_value(code, current_index, 2, parameter_modes)
    return current_index + 4

# Input
def opcode_3(code, current_index, parameter_modes):
    output_index = get_parameter_value(code, current_index, 1, parameter_modes, is_output=True)
    code[output_index] = int(input("> "))
    return current_index + 2

# Output
def opcode_4(code, current_index, parameter_modes):
    value = get_parameter_value(code, current_index, 1, parameter_modes)
    print(value)
    return current_index + 2

# Jump if true
def opcode_5(code, current_index, parameter_modes):
    value = get_parameter_value(code, current_index, 1, parameter_modes)
    if value != FALSE:
        return get_parameter_value(code, current_index, 2, parameter_modes)
    return current_index + 3

# Jump if false
def opcode_6(code, current_index, parameter_modes):
    value = get_parameter_value(code, current_index, 1, parameter_modes)
    if value == FALSE:
        return get_parameter_value(code, current_index, 2, parameter_modes)
    return current_index + 3

# Less than
def opcode_7(code, current_index, parameter_modes):
    output_index = get_parameter_value(code, current_index, 3, parameter_modes, is_output=True)
    if get_parameter_value(code, current_index, 1, parameter_modes) < get_parameter_value(code, current_index, 2, parameter_modes):
        code[output_index] = TRUE
    else:
        code[output_index] = FALSE
    return current_index + 4

# Equals
def opcode_8(code, current_index, parameter_modes):
    output_index = get_parameter_value(code, current_index, 3, parameter_modes, is_output=True)
    if get_parameter_value(code, current_index, 1, parameter_modes) == get_parameter_value(code, current_index, 2, parameter_modes):
        code[output_index] = TRUE
    else:
        code[output_index] = FALSE
    return current_index + 4

# Exit
def opcode_99(code, current_index, parameter_modes):
    return EXIT_STATUS

PARAMETER_MODE_MAP = {
    0 : parammode_0,
    1 : parammode_1
}

OPCODE_MAP = {
    1 : opcode_1,
    2 : opcode_2,
    3 : opcode_3,
    4 : opcode_4,
    5 : opcode_5,
    6 : opcode_6,
    7 : opcode_7,
    8 : opcode_8,
    99 : opcode_99
}

def read_code(file):
    with open(file, "r") as f:
        string_codes = f.read().split(',')
        result = []
        for code in string_codes:
            result.append(int(code))
        return result

def run_code(code):
    index = 0
    while index < len(code):
        full_opcode = code[index]
        opcode, parameter_modes = parse_opcode(full_opcode)
        result = OPCODE_MAP[opcode](code, index, parameter_modes)
        if result == EXIT_STATUS:
            break
        index = result