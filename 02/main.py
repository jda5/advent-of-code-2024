from utils import load_input

reports = load_input('02')


def is_safe(a: int, b: int, is_increasing: bool) -> bool:
    diff = b - a
    if is_increasing ^ (diff > 0) or not (1 <= abs(diff) <= 3):
        return False    
    return True

def is_safe_report(report: tuple[int]) -> int:
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
        report = tuple(map(int, report.split()))
        num_safe += is_safe_report(report)

    return num_safe


    

# def puzzle_two() -> int:
#     # the same rules apply as before, except if removing a single level from an 
#     # unsafe report would make it safe, the report instead counts as safe.
#     num_unsafe = 0

#     for report in reports:
#         report = tuple(map(int, report.split()))
        
#         for i in range(len(report) - 2):
#             a, b, c = report[i], report[i + 1], report[i + 2]
#             if a < b < c:
#                 is_increasing = True
#                 break
#             elif c < b < a:
#                 is_increasing = False
#                 break
#         else:
#             num_unsafe += 1
#             continue
        
#         i = 0
#         level_removed = False

#         while i < len(report) - 2:
            
#             a, b, c = report[i], report[i + 1], report[i + 2]

#             if is_safe(a, b, is_increasing):
#                 if is_safe(b, c, is_increasing):
#                     i += 1

#                 elif not level_removed:
#                     if is_safe(a, c, is_increasing):
#                         level_removed = True
#                         i += 2
#                     else:
#                         num_unsafe += 1
#                         break
#                 else:
#                     num_unsafe += 1
#                     break
            
#             elif not level_removed:
#                 if is_safe(b, c, is_increasing):
#                     i += 1

#                 elif is_safe(a, c, is_increasing):
#                     i += 2

#                 else:
#                     num_unsafe += 1
#                     break

#                 level_removed = True
            
#             else:
#                 num_unsafe += 1
#                 break

#     return len(reports) - num_unsafe



if __name__ == "__main__":
    print(puzzle_one())
    # print(puzzle_two())
