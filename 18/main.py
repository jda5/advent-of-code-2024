from utils import load_input_lines
from typing import Iterator
from queue import PriorityQueue
from collections import defaultdict

_input = load_input_lines('18')

def split_input_rows(x: str):
    values = x.split(',')
    return int(values[0]), int(values[1])

class Maze:

    VALID_DIRECTIONS = (
        (0, 1), (0, -1), (1, 0), (-1, 0)
    )

    def __init__(self, height: int, width: int):
        self.grid = [[1 for _ in range(width)] for _ in range(height)]
        self.end = (height - 1, width - 1)
        self._byte_positions = list(map(split_input_rows, _input))
        self._byte_index = 0

    def on_grid(self, row: int, col: int) -> bool:
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0])

    def get_tiles(self) -> Iterator[tuple[str, int, int]]:
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                yield self.grid[row][col], row, col

    def get_adjacent(self, pos: tuple[int, int]) -> Iterator[tuple[int, int]]:
        for dy, dx in self.VALID_DIRECTIONS:
            nrow = dy + pos[0]
            ncol = dx + pos[1]
            if self.on_grid(nrow, ncol) and bool(self.grid[nrow][ncol]):
                yield nrow, ncol

    def add_bytes(self, num: int):
        while self._byte_index < len(self._byte_positions) and num > 0:
            col, row = self._byte_positions[self._byte_index]
            self.grid[row][col] = 0
            self._byte_index += 1
            num -= 1
        self._byte_index = min(self._byte_index, len(self._byte_positions) - 1)

    def remove_bytes(self, num: int):
        while self._byte_index >= 0 and num > 0:
            col, row = self._byte_positions[self._byte_index]
            self.grid[row][col] = 1
            self._byte_index -= 1
            num -= 1
        self._byte_index = max(self._byte_index, 0)

    def print_maze(self, path: list[tuple[int, int]]):
        # Create a mutable copy of the maze
        table = {0: '#', 1: '.'}
        res = [[table[tile] for tile in row] for row in self.grid]
        
        # Mark the path taken with '@'
        for srow, scol in path:
            res[srow][scol] = '@'
        
        # Join rows and print the maze
        for row in res:
            print(''.join(row))
            
class Head:

    def __init__(self, pos: tuple[int, int], length: int = 0):
        self.pos = pos
        self.length = length

    def __lt__(self, other: 'Head') -> bool:
        return self.length < other.length
    
def shortest_path_lenth(maze: Maze) -> int | None:

    path_queue = PriorityQueue()
    path_queue.put(Head(pos=(0, 0)))

    # Use a BFS approach to navigate the maze - prioritising
    # the path with the lowest score.
    visited = {}

    while not path_queue.empty():
        head: Head = path_queue.get()
        adjacent_squares = maze.get_adjacent(head.pos)
        
        if head.pos in visited:
            if visited[head.pos] <= head.length:
                # This tile has already been visited and can be visited in fewer steps.
                # Don't continue to explore this route.
                continue
        visited[head.pos] = head.length

        if head.pos == maze.end:
            continue

        for new_pos in adjacent_squares:
            path_queue.put(Head(pos=new_pos, length=head.length + 1))
    try:
        return visited[maze.end]
    except KeyError:
        return None


def puzzle_one() -> int:
    maze = Maze(71, 71)
    maze.add_bytes(1024)
    return shortest_path_lenth(maze)
    
def puzzle_two() -> int:
    # Couple of approaches we could take, but I like the binary search approach here
    maze = Maze(71, 71)
    left, right = 1024, len(maze._byte_positions) - 1
    maze.add_bytes(left)

    while left < right - 1:
        mid = (right - left) // 2
        maze.add_bytes(mid)
        path_length = shortest_path_lenth(maze)
        if path_length:
            left = left + mid
        else:
            right = left + mid
            maze.remove_bytes(mid)
    
    return ','.join(map(str,maze._byte_positions[left]))

if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
