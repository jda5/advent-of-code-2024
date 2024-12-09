from utils import load_input_lines
from typing import Iterable
from collections import defaultdict

antenna_map = load_input_lines('08')


def get_antennae() -> Iterable[tuple[int, int, str]]:
    for row in range(len(antenna_map)):
        for col in range(len(antenna_map[0])):
            value = antenna_map[row][col]
            if value != '.':
                yield row, col, value

def on_map(row: int, col: int) -> bool:
    return 0 <= row < len(antenna_map) and 0 <= col < len(antenna_map[0])

def puzzle_one() -> int:
    # Strategy: collect the locations of each of the antenna,
    # then calculate the distance between each.
    # Use this distance to determine the location of the antinodes,
    # If the antinode is on the map increment the result by one.
    antinode_positions = set()

    antenna_positions = defaultdict(list)
    for row, col, value in get_antennae():
        antenna_positions[value].append((row, col))

    for value, positions in antenna_positions.items():
        for i in range(len(positions)):
            pos_a = positions[i]
            for j in range(i + 1, len(positions)):
                pos_b = positions[j]
                dy = pos_b[0] - pos_a[0]    # Differences in rows
                dx = pos_b[1] - pos_a[1]    # Differences in columns
                
                antinode_one = (pos_b[0] + dy, pos_b[1] + dx)
                if on_map(antinode_one[0], antinode_one[1]):
                    antinode_positions.add(antinode_one)

                antinode_two = (pos_a[0] - dy, pos_a[1] - dx)
                if on_map(antinode_two[0], antinode_two[1]):
                    antinode_positions.add(antinode_two)

    return len(antinode_positions)

def puzzle_two() -> int:
    # Basically the same as puzzle one, just with a while loop.
    antinode_positions = set()

    antenna_positions = defaultdict(list)
    for row, col, value in get_antennae():
        antenna_positions[value].append((row, col))

    for value, positions in antenna_positions.items():
        for i in range(len(positions)):
            pos_a = positions[i]
            for j in range(i + 1, len(positions)):
                pos_b = positions[j]
                dy = pos_b[0] - pos_a[0]    # Differences in rows
                dx = pos_b[1] - pos_a[1]    # Differences in columns

                antinode_one = (pos_b[0] + dy, pos_b[1] + dx)
                while on_map(antinode_one[0], antinode_one[1]):
                    antinode_positions.add(antinode_one)
                    antinode_one = (antinode_one[0] + dy, antinode_one[1] + dx)

                antinode_two = (pos_a[0] - dy, pos_a[1] - dx)
                while on_map(antinode_two[0], antinode_two[1]):
                    antinode_positions.add(antinode_two)
                    antinode_two = (antinode_two[0] - dy, antinode_two[1] - dx)

                # antinode occurs at any grid position exactly in line with at least two antennas
                # ..... this includes the antennas we are aligning!
                antinode_positions.add(pos_a)
                antinode_positions.add(pos_b)

    return len(antinode_positions)


if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
