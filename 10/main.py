from typing import Iterator
from utils import load_input_lines

input = load_input_lines('10')
map = [[int(x) if x != '.' else None for x in row] for row in input]


def on_map(map: list[list[int | None]], row: int, col: int):
    return 0 <= row < len(map) and 0 <= col < len(map[0])

def get_adjacent(map: list[list[int | None]], row: int, col: int) -> Iterator[tuple[int | None, int, int]]:
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nrow, ncol = row + dx, col + dy
        if on_map(map, nrow, ncol):
            yield map[nrow][ncol], nrow, ncol

def puzzle_one() -> int:
    total_score = 0
    for row in range(len(map)):
        for col in range(len(map[0])):
            value = map[row][col]
            if value != 0:
                continue
            
            # 9-height positions
            trails = set()

            # Start of a trail - use DFS
            stack = [(value, row, col)]

            while stack:
                curr = stack.pop()
                val = curr[0]
                if val == 9:
                    # We've found a complete trail!
                    trails.add((curr[1], curr[2]))
                else:
                    for adj in get_adjacent(map, curr[1], curr[2]):
                        if adj is not None and (val + 1 == adj[0]):
                            stack.append(adj)

            total_score += len(trails)

    return total_score

def puzzle_two() -> int:
    # Basically the same as puzzle one.
    rating = 0
    for row in range(len(map)):
        for col in range(len(map[0])):
            value = map[row][col]
            if value != 0:
                continue

            # Start of a trail - use DFS
            stack = [(value, row, col)]

            while stack:
                curr = stack.pop()
                val = curr[0]
                if val == 9:
                    # We've found a complete trail!
                    rating += 1
                else:
                    for adj in get_adjacent(map, curr[1], curr[2]):
                        if adj is not None and (val + 1 == adj[0]):
                            stack.append(adj)

    return rating


if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
