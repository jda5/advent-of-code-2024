from utils import load_input_full
from typing import Iterator

disk_map = list(map(int, load_input_full('09')))

enumerate
# The disk map uses a dense format to represent the layout of files and free space on the disk. 
# The digits alternate between indicating the length of a file and the length of free space.

def get_file_index(i: int) -> int:
    return i // 2

def checksum(arr: list[int]) -> int:
    val = 0
    for i, elem in enumerate(arr):
        if elem is not None:
            val += (elem * i)
    return val
    

def puzzle_one() -> int:
    # Strategy: use two pointers, one for the left and right of the disk map.
    i, j = 0, len(disk_map) - 1

    if len(disk_map) % 2 == 0:
        # The right index indicates to free space
        j -= 1

    res = []

    # Track how many we have inserted into the array from the right
    right_insert_count = 0

    while i < j:
        if i % 2 == 0:
            file_index = get_file_index(i)
            for _ in range(disk_map[i]):
                res.append(file_index)
        else:
            num_free = disk_map[i]
            while num_free > 0:
                if right_insert_count >= disk_map[j]:
                    j -= 2
                    right_insert_count = 0
                res.append(get_file_index(j))
                right_insert_count += 1
                num_free -= 1
        i += 1

    # After reaching the end of the above while loop, there nothing but free space.
    # Add any remaining digits to the list.
    while right_insert_count < disk_map[j]:
        res.append(get_file_index(j))
        right_insert_count += 1

    return checksum(res)

def print_disk(disk):
    temp = [str(item) if item is not None else '.' for item in disk ]
    print(''.join(temp))
    # print(''.join(temp) == '00992111777.44.333....5555.6666.....8888..')

# 6415666502672 -- too high
# 6415597058749 -- wrong
def puzzle_two() -> int:

    disk = []
    for i in range(len(disk_map)):
        if i % 2 == 0:
            file_index = get_file_index(i)
            for _ in range(disk_map[i]):
                disk.append(file_index)
        else:
            for _ in range(disk_map[i]):
                disk.append(None)

    curr_file = None
    file_count = 0

    for i in range(len(disk) - 1, -1, -1):
        file = disk[i]
        
        if curr_file != file:
            if curr_file is not None:
            
                space_count = 0
                space_index = None

                for j in range(len(disk)):
                    if j >= i + file_count:
                        space_index = None
                        break

                    space = disk[j]
                    if space is None:
                        space_count += 1
                        if space_count == file_count:
                            space_index = j - (space_count - 1)
                            break
                    else:
                        space_count = 0
                
                # print("File:", curr_file)
                # print("File Count:", file_count)
                # print("Space Count:", space_count)
                # print("Space Index:", space_index)

                if space_index:
                    for k in range(file_count):
                        # print(k)
                        # print(space_index + k, i + 1 + k)
                        # print(space_index)
                        # print(k)
                        # print(space_index + k)
                        # print("K :", k)
                        # print("Space Index: ", space_index)
                        disk[space_index + k] = curr_file
                        disk[i + 1 + k] = None

                # print(file_count, space_count, curr_file, space_index)
                # print_disk(disk)

            file_count = 1
            curr_file = file

        else:
            file_count += 1

    return checksum(disk)
                

if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
