from utils import load_input_lines
from math import prod
from scipy.stats import zscore
import numpy as np

_input = load_input_lines('14')


class Robot:

    def __init__(self, pos: list[int, int], vel: tuple[int, int]):
        self.pos = pos
        self.vel = vel

    @property
    def col(self):
        return self.pos[0]

    @property
    def row(self):
        return self.pos[1]

class Map:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.robots: list[Robot] = []

    def __str__(self) -> str:
        counts = [0] * (self.width * self.height)

        # Count the number of robots in each cell
        for robot in self.robots:
            counts[robot.row * self.width + robot.col] += 1

        # Build lines from counts
        lines = []
        start = 0
        for _ in range(self.height):
            row_counts = counts[start:start + self.width]
            line = "".join(str(c) if c > 0 else '.' for c in row_counts)
            lines.append(line)
            start += self.width

        return "\n".join(lines)

    def add_robot(self, robot: Robot):
        self.robots.append(robot)

    def move_robots(self):
        for robot in self.robots:
            robot.pos[0] = (robot.pos[0] + robot.vel[0]) % self.width
            robot.pos[1] = (robot.pos[1] + robot.vel[1]) % self.height

    def calculate_safety_factor(self):
        height_window = self.height // 2
        width_window = self.width // 2
        quadrants = [[0, 0], [0, 0]]
        for robot in self.robots:
            # Robots that are exactly in the middle (horizontally or vertically) don't count as being in any quadrant
            if robot.row == height_window or robot.col == width_window:
                continue
            i = int(robot.row >= height_window)
            j = int(robot.col >= width_window)
            quadrants[i][j] += 1
        safety_factor = 1
        for quads in quadrants:
            safety_factor *= prod(quads)
        return safety_factor

def load_map() -> Map:
    _map = Map(width=101, height=103)
    for line in _input:
        pos, vel = line.split()
        x, y = pos[2:].split(',')
        dx, dy = vel[2:].split(',')
        _map.add_robot(Robot(pos=[int(x), int(y)], vel=(int(dx), int(dy))))
    return _map

def puzzle_one() -> int:
    _map = load_map()
    for _ in range(100):
        _map.move_robots()
    return _map.calculate_safety_factor()

def puzzle_two() -> int:
    _map = load_map()
    safety_factors = []
    for i in range(10_000):
        # A map with a christmas tree might have a very low safety factor.
        _map.move_robots()
        safety_factor = _map.calculate_safety_factor()
        safety_factors.append(safety_factor)

    # Find outlying safety scores by calculating their Z-scores.
    z_scores = zscore(safety_factors)
    return np.argmin(z_scores) + 1

if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
