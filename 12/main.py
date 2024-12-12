from utils import load_input_lines
from typing import Iterator

plot = load_input_lines('12')


def get_plot_squares() -> Iterator[tuple[str, int, int]]:
    # Iterates over all squares in the plot and yields their value and coordinates.
    for row in range(len(plot)):
        for col in range(len(plot[0])):
            yield plot[row][col], row, col

def on_plot(row: int, col: int):
    # Checks whether the given coordinates are within the boundaries of the plot.
    return 0 <= row < len(plot) and 0 <= col < len(plot[0])

def get_adjacent(row: int, col: int) -> Iterator[tuple[str, int, int]]:
    # Yields adjacent squares and their coordinates. If a square is outside the plot,
    # yields None values to signal the edge of the plot.
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nrow, ncol = row + dx, col + dy
        if on_plot(nrow, ncol):
            yield plot[nrow][ncol], nrow, ncol
        else:
            yield None, None, None

def puzzle_one() -> int:
    visited = set()
    total_cost = 0

    for value, row, col in get_plot_squares():
        loc = (row, col)

        if loc not in visited:
            visited.add(loc)
            area = 1
            perimeter = 0

            stack = [loc]
            while stack:
                curr_row, curr_col = stack.pop()

                for adj_val, adj_row, adj_col in get_adjacent(curr_row, curr_col):
                    adj_loc = (adj_row, adj_col)

                    if adj_val != value:
                        perimeter += 1
                    elif adj_loc not in visited:
                        area += 1
                        visited.add(adj_loc)
                        stack.append(adj_loc)

            total_cost += area * perimeter

    return total_cost

def get_num_corners(shape: set[tuple[int, int]], row: int, col: int) -> int:
    # Calculates the number of corners for a given square within the shape.
    # A corner is identified based on the diagonals and neighboring squares:
    # - If the diagonal is not part of the shape, and both neighboring squares
    #   (one from the row and one from the column) are either inside or outside
    #   the shape, it is considered a corner.
    corners = 0
    
    for dx, dy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        diagonal_row = row + dx
        diagonal_col = col + dy

        # To get the neightbouring squares of the current square and its diagonals
        # we swap the rows and the columns
        neighbour_one = (row, diagonal_col)
        neighbour_two = (diagonal_row, col)

        if (diagonal_row, diagonal_col) in shape:
            # The diagonal is part of the shape. This can only be a corner piece if
            # the neighbouring squares aren't part of the shape.
            if (neighbour_one not in shape) and (neighbour_two not in shape):
                corners += 1
        
        # XOR: True/True -> False | False/False -> False
        elif not ((neighbour_one in shape) ^ (neighbour_two in shape)):
            corners += 1

    return corners

def puzzle_two() -> int:
    # The number of corners of a ploygon equals the number of sides.
    # calculating the total cost based on the number of corners and the size of each shape.

    visited = set()
    total_cost = 0

    for value, row, col in get_plot_squares():
        loc = (row, col)

        if loc not in visited:
            shape = {loc}
            visited.add(loc)

            stack = [loc]
            while stack:
                curr_row, curr_col = stack.pop()

                for adj_val, adj_row, adj_col in get_adjacent(curr_row, curr_col):
                    adj_loc = (adj_row, adj_col)

                    if adj_val == value and adj_loc not in shape:
                        shape.add(adj_loc)
                        visited.add(adj_loc)
                        stack.append(adj_loc)

            num_corners = sum(get_num_corners(shape, square[0], square[1]) for square in shape)
            total_cost += num_corners * len(shape)

    return total_cost


if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
