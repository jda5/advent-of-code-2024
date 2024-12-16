from utils import load_input_lines
from typing import Iterator
from queue import PriorityQueue


_input = load_input_lines('16')

class Maze:

    def __init__(self, map: list[str]):
        self.map = map
        self.end_pos = self.get_square_pos('E')

    def get_tiles(self) -> Iterator[tuple[str, int, int]]:
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                yield self.map[row][col], row, col

    def get_adjacent(self, pos: tuple[int, int], prev: tuple[int, int]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        directions = (
            (0, 1), (0, -1), (1, 0), (-1, 0)
        )
        adjacent = []
        for dy, dx in directions:
            nrow = dy + pos[0]
            ncol = dx + pos[1]
            if self.map[nrow][ncol] != '#' and (nrow, ncol) != prev:
                adjacent.append(((nrow, ncol), (dy, dx)))
        return adjacent

    def get_square_pos(self, square: str) -> tuple[int, int]:
        for value, row, col in self.get_tiles():
            if value == square:
                return row, col
            
    def print_maze(self, steps: list[tuple[int, int]]):
        # Create a mutable copy of the maze
        res = [list(row) for row in self.map]
        
        # Mark the path taken with '@'
        for srow, scol in steps:
            if res[srow][scol] not in ('S', 'E'):  # Preserve start and end markers
                res[srow][scol] = '@'
        
        # Join rows and print the maze
        for row in res:
            print(''.join(row))
            
class Head:

    def __init__(self, pos: tuple[int, int], direction: tuple[int, int], score: int, prev: tuple[int, int]):
        self.pos = pos
        self.direction = direction
        self.score = score
        self.prev = prev

    def __lt__(self, other: 'Head') -> bool:
        return self.score < other.score


def puzzle_one() -> int:
    maze = Maze(_input)
    reindeer_pos = maze.get_square_pos('S')

    # Prioritise paths with the lowest score.
    path_queue = PriorityQueue()
    path_queue.put(
        Head(pos=reindeer_pos, direction=(0, 1), score=0, prev=reindeer_pos)
    )

    # Use a BFS approach to navigate the maze - prioritising
    # the path with the lowest score.
    visited_scores = {}

    while not path_queue.empty():
        head: Head = path_queue.get()
        adjacent_squares = maze.get_adjacent(head.pos, head.prev)
        
        if head.pos in visited_scores:
            if visited_scores[head.pos] <= head.score and len(adjacent_squares) <= 1:
                # This tile has already been visited and has a lower score.
                # Don't continue to explore this route.
                continue
        visited_scores[head.pos] = head.score

        if head.pos == maze.end_pos:
            continue

        for new_pos, new_direction in adjacent_squares:
            
            # Calculate the score the path would have, if went to this next square
            if new_direction != head.direction:
                new_score = head.score + 1001
            else:
                new_score = head.score + 1

            path_queue.put(
                Head(pos=new_pos, direction=new_direction, score=new_score, prev=head.pos)
            )
    
    return visited_scores[maze.end_pos]

def puzzle_two() -> int:
    ...


if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())

# 82460
# 590
