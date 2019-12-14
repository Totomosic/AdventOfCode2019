def parse_range(file):
    with open(file, "r") as f:
        text = f.read().replace('\n', '').replace('\r', '')
        parts = text.split('-')
        return int(parts[0]), int(parts[1])

def is_valid_password(password, range):
    string = str(password)
    if len(string) != 6:
        return False
    if password < range[0] or password > range[1]:
        return False
    prevInt = None
    double = False
    for c in string:
        i = int(c)
        if i == prevInt:
            double = True
        if prevInt is not None and i < prevInt:
            return False
        prevInt = i
    if not double:
        return False
    return True

def is_valid_password_v2(password, range):
    string = str(password)
    if len(string) != 6:
        return False
    if password < range[0] or password > range[1]:
        return False
    prevInt = None
    double = False
    doubleCount = 1
    for c in string:
        i = int(c)
        if i == prevInt:
            doubleCount += 1
        else:
            if not double:
                double = doubleCount == 2
            doubleCount = 1
        if prevInt is not None and i < prevInt:
            return False
        prevInt = i
    if not double and doubleCount == 2:
        double = True
    if not double:
        return False
    return True

min, max = parse_range("range.txt")

count = 0
for i in range(min, max + 1):
    if is_valid_password(i, (min, max)):
        count += 1
print("Day 4 - Part 1")
print(count)
print(count == 460)

count = 0
for i in range(min, max + 1):
    if is_valid_password_v2(i, (min, max)):
        count += 1
print("Day 4 - Part 2")
print(count)
print(count == 290)