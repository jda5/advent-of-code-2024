from utils import load_input_full
from functools import cache

_input = load_input_full('11')


@cache
def apply_rules(n: int):
    # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    if n == 0:
        return [1]
    
    # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones
    string_num = str(n)
    if len(string_num) % 2 == 0:
        l = len(string_num) // 2
        # The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved 
        # on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
        return [int(string_num[:l]), int(string_num[l:])]

    # If none of the other rules apply, the stone is replaced by a new stone; 
    # the old stone's number multiplied by 2024 is engraved on the new stone.
    return [n * 2024]

@cache
def calculate_num_stones(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1
    
    transformed_stones = apply_rules(stone)
    return sum(calculate_num_stones(num, blinks - 1) for num in transformed_stones)

def puzzle_one() -> int:
    total_stones = 0
    stones = list(map(int, _input.split()))
    for stone in stones:
        total_stones += calculate_num_stones(stone, 25)
    return total_stones


def puzzle_two() -> int:
    total_stones = 0
    stones = list(map(int, _input.split()))
    for stone in stones:
        total_stones += calculate_num_stones(stone, 75)
    return total_stones


if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
