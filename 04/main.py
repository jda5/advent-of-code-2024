from utils import load_input_lines, load_input_full

word_search = load_input_lines('04')

NUM_ROWS = len(word_search)
NUM_COLS = len(word_search[0])


def count_target_word_occurances(
    word: str, 
    start_row: int, 
    start_col: int, 
    directions: tuple[tuple[int, int]]
) -> int:

    occurances = 0

    if word_search[start_row][start_col] != word[0]:
        return occurances

    for dx, dy in directions:

        # First, determine whether we can even build a word of sufficient length in
        # this given direction.
        final_row = start_row + (dx * (len(word) - 1))
        final_col = start_col + (dy * (len(word) - 1))

        if 0 <= final_row < NUM_ROWS and 0 <= final_col < NUM_COLS:
            # We can build a word of sufficient length.
            row = start_row
            col = start_col

            for i in range(len(word) - 1):
                row += dx
                col += dy
                if word_search[row][col] != word[i + 1]:
                    break
            else:
                occurances += 1
                
    return occurances

def puzzle_one() -> int:
    directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    count = 0
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            count += count_target_word_occurances('XMAS', row, col, directions)

    return count

def puzzle_two() -> int:
    directions = {
        (1, 1): (-1, -1),
        (-1, -1): (1, 1),
        (1, -1): (-1, 1),
        (-1, 1): (1, -1)
    }
    
    count = 0
    for row in range(1, NUM_ROWS - 1):
        for col in range(1, NUM_COLS - 1):
            if word_search[row][col] == 'A':

                mas_count = 0
                for m, s in directions.items():
                    m_row, m_col = row + m[0], col + m[1]
                    s_row, s_col= row + s[0], col + s[1]
                    if word_search[m_row][m_col] == 'M' and word_search[s_row][s_col] == 'S':
                        mas_count += 1
                
                if mas_count > 1:
                    count += 1

    return count

if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
