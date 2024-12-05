from utils import load_input_full
from collections import defaultdict

input = load_input_full('05')

ordering_rules, updates = input.split('\n\n')

def split_and_format(row: str, sep: str) -> list[int]:
    return [int(item) for item in row.split(sep)]

ordering_rules = [split_and_format(row, '|') for row in ordering_rules.split('\n')]
updates = [split_and_format(row, ',') for row in updates.split('\n')]

class Rule:

    def __init__(self, value: int):
        self.value = value
        self.before = set()
        self.after = set()

    def check_list_after(self, pages: list[int]) -> bool:
        for page in pages:
            if page in self.before:
                return False
        return True
    

def create_rules():
    rules = dict()
    for before, after in ordering_rules:
        if before not in rules:
            rules[before] = Rule(before)
        rules[before].after.add(after)

        if after not in rules:
            rules[after] = Rule(after)
        rules[after].before.add(before)
    return rules

def is_correct_order(pages: list[int], rules: dict[Rule]):
    for i, page in enumerate(pages):
        if page not in rules:
            continue
        rule: Rule = rules[page]
        pages_after = pages[i+1:]
        correct_order = rule.check_list_after(pages_after)
        if not correct_order:
            return False
    return True
            
def puzzle_one() -> int:
    middle_sum = 0
    rules = create_rules()
    for pages in updates:
        if is_correct_order(pages, rules):
            middle_sum += pages[len(pages) // 2]

    return middle_sum

def page_sort(pages: list[int], rules: dict[Rule]):
    # A modification of the quick sort algorithm

    before = []
    equal = []
    after = []

    if len(pages) > 1:
        pivot = pages[0]
        rule: Rule = rules[pivot]
        
        for page in pages:
            if page in rule.before:
                before.append(page)

            elif page == rule.value:
                equal.append(page)

            elif page in rule.after:
                after.append(page)

        return page_sort(before, rules) + equal + page_sort(after, rules) 
    else:
        return pages

def puzzle_two() -> int:
    middle_sum = 0
    rules = create_rules()
    for pages in updates:
        if not is_correct_order(pages, rules):
            # Collect the page numbers for which we have rules and sort them
            sorted_pages = page_sort([page for page in pages if page in rules], rules)

            # Iterate over the original array of pages and swap the page number
            # for which we have rules, so that they are in the correct order.
            j = 0
            for i, page in enumerate(pages):
                if page in rules:
                    pages[i] = sorted_pages[j]
                    j += 1

            middle_sum += pages[len(pages) // 2]

    return middle_sum

if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
