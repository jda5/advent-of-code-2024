from collections import Counter
from utils import load_input_lines

location_ids = load_input_lines('01')

def puzzle_one() -> int:
    left, right = [], []
    for location in location_ids:
        l, r = location.split()
        left.append(int(l))
        right.append(int(r))

    distance = 0
    for l, r in zip(sorted(left), sorted(right)):
        distance += abs(l - r)
    
    return distance

def puzzle_two() -> int:
    left, right_counts = [], Counter()
    for location in location_ids:
        l, r = location.split()
        left.append(int(l))
        right_counts[int(r)] += 1
    
    score = 0
    for elem in left:
        score += right_counts.get(elem, 0) * elem
    
    return score
    

if __name__ == "__main__":
    print(puzzle_two())