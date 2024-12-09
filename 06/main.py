from typing import Iterator
from utils import load_input_lines

_input = load_input_lines('06')


class Map:

    def __init__(self, map: list[str]):
        self.map = [[col for col in row] for row in map]
        self.obstruction = (None, None)

    def tiles(self) -> Iterator[tuple[int, int, str]]:
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                yield row, col, self.map[row][col]

    def on_map(self, row: int, col: int) -> bool:
        return (0 <= row < len(self.map)) and (0 <= col < len(self.map[0]))
    
    def get(self, row: int, col: int) -> str | None:
        if not self.on_map(row, col):
            return None
        return self.map[row][col]
    
    def move(self, guard, row: int, col: int):
        self.map[row][col] = '^'
        self.map[guard.pos[0]][guard.pos[1]] = '.'
        guard.pos = (row, col)

    def reset(self, guard):
        self.map[guard.pos[0]][guard.pos[1]] = '.'
        if self.obstruction[0] is not None:
            self.map[self.obstruction[0]][self.obstruction[1]] = '.'
        self.map[guard.initial_pos[0]][guard.initial_pos[1]] = '^'
        
    def place_obstruction(self, row: int, col: int):
        self.map[row][col] = '#'
        self.obstruction = (row, col)

class Guard:

    # N, E, S, W
    WALKING_DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))

    def __init__(self, pos: tuple[int, int]):
        self.initial_pos = pos
        self.pos = pos
        self.dir = 0

    @classmethod
    def init(cls, map: Map) -> 'Guard':
        for row, col, tile in map.tiles():
            if tile == '^':
                return cls((row, col))

    def step(self) -> tuple[int, int]:
        dir = self.WALKING_DIRECTIONS[self.dir]
        dx = self.pos[0] + dir[0]
        dy = self.pos[1] + dir[1]
        return dx, dy
    
    def rotate(self):
        self.dir = (self.dir + 1) % len(self.WALKING_DIRECTIONS)

    def reset(self):
        self.pos = self.initial_pos
        self.dir = 0


def puzzle_one() -> set[tuple[int, int]]:
    distinct_positions = set()
    
    # Walk forwards
    map = Map(_input)
    guard = Guard.init(map)
    distinct_positions.add(guard.pos)

    while map.on_map(*guard.pos):
        dx, dy = guard.step()
        tile = map.get(dx, dy)
        if tile is None:
            break
        
        if tile == '#':
            guard.rotate()

        elif tile == '.':
            map.move(guard, dx, dy)
            distinct_positions.add(guard.pos)

    return distinct_positions
            
# Solution takes about 11 seconds to compute
def puzzle_two() -> int:
    """
    Notes and observations:

    A cycle is caused when the guard returns to one of positions they have visited
    and are facing the same direction.

    To speed things up, we can find all unique positions (and directions) and place
    an obstacle in front of the guard - then track his movements.
    """
    # First get all positions that the guard will be in - these
    # are the positions on which we will place objects.
    distinct_positions = puzzle_one()

    map = Map(_input)
    guard = Guard.init(map)

    num_cycles = 0

    for row, col in distinct_positions:
        # Don't place the obstruction directly on the guards head.
        if (row, col) == guard.initial_pos:
            continue

        map.reset(guard)
        guard.reset()
        map.place_obstruction(row, col)

        # Guard positions and facing directions
        position_direction = set()

        # Walk through the map until we leave or hit a cycle
        while map.on_map(*guard.pos):

            dx, dy = guard.step()
            tile = map.get(dx, dy)
            if tile is None:
                break

            if (guard.pos, guard.dir) in position_direction:
                num_cycles += 1
                break
            
            if tile == '#':
                guard.rotate()

            elif tile == '.':
                position_direction.add((guard.pos, guard.dir))
                map.move(guard, dx, dy)

    return num_cycles
        


if __name__ == "__main__":
    print(len(puzzle_one()))
    print(puzzle_two())
