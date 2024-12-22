from utils import load_input_lines, load_input_full

input = load_input_full()

class DirectionalKeypad:

    MOVEMENT_TABLE = {
        '<': {
            '<': '',
            '>': '>>',
            '^': '>^',
            'v': '>',
            'A': '>^>'
        },
        '>': {
            '<': '<<',
            '>': '',
            '^': '<^',
            'v': '<',
            'A': '^'
        },
        '^': {
            '<': 'v<',
            '>': 'v>',
            '^': '',
            'v': 'v',
            'A': '>'
        },
        'v': {
            '<': '<',
            '>': '>',
            '^': '^',
            'v': '',
            'A': '>^'
        },
        'A': {
            '<': '<v<',
            '>': 'v',
            '^': '<',
            'v': '<v',
            'A': ''
        }
    }

    def __init__(self):
        self.pos = "A"
        self.movements = []

    def get_movements(self, button: str):
        return self.MOVEMENT_TABLE[self.pos][button]

def puzzle_one() -> int:
    ...

def puzzle_two() -> int:
    ...


if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
