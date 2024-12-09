from utils import load_input_lines

input = load_input_lines('07')


def get_combinations(target: int, values: list[int], curr: int, i: int) -> int:
    if curr > target:
        return 0
    
    if i == len(values):
        if int(curr == target):
            return target
        return 0
    
    if i < 2:
        return get_combinations(target, values, values[0] + values[1], 2) + get_combinations(target, values, values[0] * values[1], 2)
    return get_combinations(target, values, curr + values[i], i + 1) + get_combinations(target, values, curr * values[i], i + 1)

def puzzle_one() -> int:
    res = 0
    for test in input:
        array = test.split()
        target = int(array[0][:-1])
        values = list(map(int, array[1:]))
        if get_combinations(target, values, 0, 0):
            res += target
    return res

def concatenate(a: int, b: int) -> int:
    return int(f"{a}{b}")

def combinations_concatenation(target: int, values: list[int], curr: int, i: int) -> int:
    if curr > target:
        return 0
    
    if i == len(values):
        if int(curr == target):
            return target
        return 0
    
    if i < 2:
        return combinations_concatenation(target, values, values[0] + values[1], 2) \
                + combinations_concatenation(target, values, values[0] * values[1], 2) \
                + combinations_concatenation(target, values, concatenate(values[0], values[1]), 2)
    return combinations_concatenation(target, values, curr + values[i], i + 1) \
        + combinations_concatenation(target, values, curr * values[i], i + 1) \
        + combinations_concatenation(target, values, concatenate(curr, values[i]), i + 1)

def puzzle_two() -> int:
    res = 0
    for test in input:
        array = test.split()
        target = int(array[0][:-1])
        values = list(map(int, array[1:]))
        if combinations_concatenation(target, values, 0, 0):
            res += target
    return res


if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
