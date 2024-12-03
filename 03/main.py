import re
from utils import load_input_full

input_program = load_input_full('03')


def puzzle_one(program: str) -> int:
    groups = re.findall(r"mul\((\d+),(\d+)\)", program)
    return sum(int(group[0]) * int(group[1]) for group in groups)

def find_conditional(conditional: str, start: int) -> int:
    try:
        return input_program.index(conditional, start)
    except ValueError:
        return len(input_program)

def puzzle_two() -> int:
    enabled = True
    start = 0
    res = 0

    while start < len(input_program):

        if enabled:
            end = find_conditional("don't()", start)
            res += puzzle_one(input_program[start:end])
            start = end + len("don't()")
            enabled = False
        else:
            start = find_conditional("do()", start) + len("do()")
            enabled = True

    return res

if __name__ == "__main__":
    print(puzzle_one(program=input_program))
    print(puzzle_two())
