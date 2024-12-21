from typing import Iterator
from utils import load_input_lines

_input = load_input_lines('20')


class Maze:

    VALID_DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self, grid: list[str]):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.start_position = self._find_square_position('S')

    def is_on_grid(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width
    
    def get_tile(self, pos: tuple[int, int]) -> str:
        row, col = pos
        return self.grid[row][col]

    def all_tiles(self) -> Iterator[tuple[str, int, int]]:
        for row in range(self.height):
            for col in range(self.width):
                yield self.grid[row][col], row, col

    def adjacent_tiles(self, pos: tuple[int, int]) -> Iterator[tuple[str, int, int]]:
        row, col = pos
        for drow, dcol in self.VALID_DIRECTIONS:
            new_row, new_col = row + drow, col + dcol
            if self.is_on_grid(new_row, new_col):
                yield self.grid[new_row][new_col], new_row, new_col

    def _find_square_position(self, square: str) -> tuple[int, int]:
        for tile_char, row, col in self.all_tiles():
            if tile_char == square:
                return (row, col)


class Node:

    def __init__(self, pos: tuple[int, int], order: int):
        self.pos = pos
        self.order = order
        self.next = None

    def __str__(self):
        return f"Node(order={self.order}, pos={self.pos})"


def find_cheat_positions(maze: Maze, start_pos: tuple[int, int], cheat_length: int) -> list[tuple[tuple[int, int], int]]:

    possible_positions = []
    
    # Collect potential horizontal moves within 'cheat_length'
    horizonatal_pos = [ (start_pos, cheat_length) ]

    # Move steps left or right, then leftover steps remain.
    for steps in range(1, cheat_length + 1):
        move_right = start_pos[1] + steps
        move_left = start_pos[1] - steps

        if 0 <= move_left < maze.width:
            horizonatal_pos.append(((start_pos[0], move_left), cheat_length - steps))
        if 0 <= move_right < maze.width:
            horizonatal_pos.append(((start_pos[0], move_right), cheat_length - steps))

    # For each horizontal candidate, see how far we can go vertically.
    for (candidate_row, candidate_col), remaining_steps in horizonatal_pos:
        for steps in range(0, remaining_steps + 1):
            move_up = candidate_row - steps
            move_down = candidate_row + steps
            time_cheating = cheat_length - (remaining_steps - steps)

            # If we can step up or down onto track, add to possible positions.
            if 0 <= move_up < maze.height and maze.get_tile((move_up, candidate_col)) != '#':
                possible_positions.append(((move_up, candidate_col), time_cheating))

            if 0 <= move_down < maze.height and maze.get_tile((move_down, candidate_col)) != '#' and steps > 0:
                possible_positions.append(((move_down, candidate_col), time_cheating))

    return possible_positions


def build_maze_and_path() -> tuple[Maze, Node, dict[tuple[int, int], Node]]:
    maze = Maze(_input)
    head = Node(pos=maze.start_position, order=0)
    pos_node = {head.pos: head}

    traversable_tiles = {'.', 'E'}

    curr = head
    while maze.get_tile(curr.pos) != 'E':
        for tile, row, col in maze.adjacent_tiles(curr.pos):
            if (tile in traversable_tiles) and (row, col) not in pos_node:
                curr.next = Node(pos=(row, col), order=len(pos_node))
                curr = curr.next
                pos_node[curr.pos] = curr

    return maze, head, pos_node


def puzzle_one(cheat_length=2) -> int:
   
    maze, head, pos_node = build_maze_and_path()

    total = 0
    curr = head

    while maze.get_tile(curr.pos) != 'E':
        for (cheat_row, cheat_col), time_cheating in find_cheat_positions(maze, curr.pos, cheat_length=cheat_length):
            target_node = pos_node[(cheat_row, cheat_col)]
            time_saved = target_node.order - curr.order - time_cheating
            if time_saved >= 100:
                total += 1
        curr = curr.next

    return total


def puzzle_two() -> int:
    return puzzle_one(20)


if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
