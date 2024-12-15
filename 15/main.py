from utils import load_input_full
from typing import Iterator
from collections import OrderedDict
from queue import Queue

_input = load_input_full('15')


class Map:

    DIRECTIONS = {
        '>': (0, 1),
        '^': (-1, 0),
        '<': (0, -1),
        'v': (1, 0)
    }

    def __init__(self, map: list[list[str]]):
        self.map = map
        self.robot_pos = self._get_robot_pos()

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.map])
    
    def _get_squares(self) -> Iterator[tuple[str, int, int]]:
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                yield self.map[row][col], row, col

    def _get_robot_pos(self) -> list[int, int]:
        for item, row, col in self._get_squares():
            if item == '@':
                return [row, col]

    def get_adjacent(self, pos: list[int, int], direction: tuple[int, int]) -> tuple[str, tuple[int, int]]:
        row = pos[0] + direction[0]
        col = pos[1] + direction[1]
        return self.map[row][col], (row, col)
    
    def move_items(self, item_positions: OrderedDict, direction: tuple[int, int]):
        for item_pos in reversed(item_positions):
            item = self.map[item_pos[0]][item_pos[1]]
            new_pos = (item_pos[0] + direction[0], item_pos[1] + direction[1])
            self.map[new_pos[0]][new_pos[1]] = item
            self.map[item_pos[0]][item_pos[1]] = '.'
            if item == '@':
                self.robot_pos = new_pos
                
    def gps_sum(self) -> int:
        gps = 0
        for item, row, col in self._get_squares():
            if item == 'O' or item == '[':
                gps += (100 * row) + col 
        return gps

def load_basic() -> tuple[Map, str]:
    _map, movements = _input.split('\n\n')
    _map = Map([[elem for elem in row] for row in _map.split('\n')])
    movements = movements.replace('\n', '')
    return _map, movements

def load_extended() -> tuple[Map, str]:
    _map, movements = _input.split('\n\n')
    
    map_input = []
    for input_row in _map.split('\n'):
        row = []
        for elem in input_row:
            if elem == 'O':
                row.append('[')
                row.append(']')
            elif elem == '@':
                row.append(elem)
                row.append('.')
            else:
                row.append(elem)
                row.append(elem)
        map_input.append(row)
    
    _map = Map(map_input)
    movements = movements.replace('\n', '')
    return _map, movements


def puzzle_one() -> int:
    _map, movements = load_basic()

    for movement in movements:
        direction = _map.DIRECTIONS[movement]

        item_positions = OrderedDict()
        item_positions[tuple(_map.robot_pos)] = None
        queue = Queue()
        queue.put(_map.robot_pos)
        hit_wall = False

        while not queue.empty():

            curr_item = queue.get()
            next, pos = _map.get_adjacent(curr_item, direction)

            if next == 'O':
                item_positions[pos] = None
                queue.put(pos)

            elif next == '#':
                hit_wall = True
                break

        if not hit_wall:
            _map.move_items(item_positions, direction)
    
    return _map.gps_sum()


def puzzle_two() -> int:
    _map, movements = load_extended()
    horizontal_movements = {'>', '<'}

    for movement in movements:
        direction = _map.DIRECTIONS[movement]

        item_positions = OrderedDict()
        item_positions[tuple(_map.robot_pos)] = None
        queue = Queue()
        queue.put(_map.robot_pos)
        hit_wall = False

        while not queue.empty():

            curr_item = queue.get()
            next, pos = _map.get_adjacent(curr_item, direction)

            if next == '[' or next == ']':
                # A box! Add it to the list of items to be moved, as well as the box that closes it.
                if movement not in horizontal_movements:
                    box_side = (pos[0], pos[1] + 1) if next == '[' else (pos[0], pos[1] - 1)
                    item_positions[box_side] = None
                    queue.put(box_side)
                item_positions[pos] = None
                queue.put(pos)

            elif next == '#':
                hit_wall = True
                break

        if not hit_wall:
            _map.move_items(item_positions, direction)

    return _map.gps_sum()

if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
