from functools import cache
from utils import load_input_full

# Load and format the inputs.
_input = load_input_full('19')

patterns, designs = _input.split('\n\n', maxsplit=1)
patterns = set(patterns.strip().split(', '))
designs = designs.strip().split('\n')

@cache
def is_possible(design) -> bool:
    if len(design) == 1:
        return design in patterns
    if design in patterns:
        return True
    return any(is_possible(design[i:]) for i in range(len(designs)) if design[:i] in patterns)

def puzzle_one() -> int:
    num_possible = 0 
    for design in designs:
        num_possible += int(is_possible(design))
    return num_possible

@cache
def num_possible(design: str) -> int:
    if len(design) == 0:
        return 1
    
    total_ways = 0
    for i in range(len(design) + 1):
        prefix, suffix = design[:i], design[i:]
        if prefix in patterns:
            total_ways += num_possible(suffix)
    return total_ways

def puzzle_two() -> int:
    return sum(num_possible(design) for design in designs)


if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
