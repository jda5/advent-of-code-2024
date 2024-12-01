from os.path import abspath, dirname, join

TOP = dirname(abspath(__file__))

def load_input(puzzle_number: str) -> list[str]:
    filepath = join(TOP, puzzle_number, 'input.txt')
    with open(filepath) as file:
        return file.read().splitlines()