from typing import Iterator
from queue import PriorityQueue


with open('input.txt') as file:
    _input = file.read().splitlines()


class Maze:

    def __init__(self, map: list[str]):
        self.map = map
        self.end_pos = self.get_square_pos('E')

    def get_tiles(self) -> Iterator[tuple[str, int, int]]:
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                yield self.map[row][col], row, col

    def get_adjacent(self, pos: tuple[int, int]) -> Iterator[tuple[str, tuple[int, int], tuple[int, int]]]:
        directions = (
            (0, 1), (0, -1), (1, 0), (-1, 0)
        )
        for dy, dx in directions:
            nrow = dy + pos[0]
            ncol = dx + pos[1]
            yield self.map[nrow][ncol], (nrow, ncol), (dy, dx)

    def get_square_pos(self, square: str) -> tuple[int, int]:
        for value, row, col in self.get_tiles():
            if value == square:
                return row, col
            
class Head:

    def __init__(self, pos: tuple[int, int], direction: tuple[int, int], score: int):
        self.pos = pos
        self.direction = direction
        self.score = score

    def __lt__(self, other: 'Head') -> bool:
        return self.score < other.score


# 82464 -- Too high
def puzzle_one() -> int:
    maze = Maze(_input)
    reindeer_pos = maze.get_square_pos('S')

    # Prioritise paths with the lowest score.
    path_queue = PriorityQueue()
    path_queue.put(
        Head(pos=reindeer_pos, direction=(0, 1), score=0)
    )

    # Use a BFS approach to navigate the maze - prioritising
    # the path with the lowest score.
    visited_scores = {}

    while not path_queue.empty():
        head: Head = path_queue.get()

        for value, new_pos, new_direction in maze.get_adjacent(head.pos):
            if value == '#':
                # Wall. Can't explore this path further.
                continue
            
            # Calculate the score the path would have, if went to this next square
            if new_direction != head.direction:
                new_score = head.score + 1001
            else:
                new_score = head.score + 1

            if new_pos in visited_scores:
                if visited_scores[new_pos] <= new_score:
                    # The tile has already been visited has a score.
                    # Don't continue to explore this route.
                    continue
            
            visited_scores[new_pos] = new_score

            # Don't add this position to the search space if we've reached the end.
            if new_pos != maze.end_pos:
                path_queue.put(Head(pos=new_pos, direction=new_direction, score=new_score))
    
    return visited_scores[maze.end_pos]

def puzzle_two() -> int:
    ...


if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())

