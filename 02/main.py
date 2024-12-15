from utils import load_input_lines

reports = load_input_lines('02')


def is_safe(a: int, b: int, is_increasing: bool) -> bool:
    diff = b - a
    if (is_increasing ^ (diff > 0)) or not (1 <= abs(diff) <= 3):
        return False    
    return True

def is_safe_report(report: list[int]) -> int:
    prev = report[0]
    is_increasing = prev < report[1]
    for curr in report[1:]:
        if not is_safe(prev, curr, is_increasing):
            return 0
        prev = curr
    return 1

def puzzle_one() -> int:
    # A report only counts as safe if both of the following are true:

    # The levels are either all increasing or all decreasing.
    # Any two adjacent levels differ by at least one and at most three.
    num_safe = 0

    for report in reports:
        report = list(map(int, report.split()))
        num_safe += is_safe_report(report)

    return num_safe

def puzzle_two() -> int:
    # the same rules apply as before, except if removing a single level from an 
    # unsafe report would make it safe, the report instead counts as safe.
    num_unsafe = 0

    for report in reports:
        report = list(map(int, report.split()))
        if not is_safe_report(report):
            for i in range(len(report)):
                # Eurgh this is bad.
                if is_safe_report(report[:i] + report[i+1:]):
                    break
            else:
                num_unsafe += 1

    return len(reports) - num_unsafe

if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
