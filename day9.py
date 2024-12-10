"""disk defragmenter"""

import pathlib


def data_loader(input_file: pathlib.Path) -> str:
    with open(input_file, "r") as f:
        disk = f.readline()

    return disk


def represent_disk(disk: str):
    expanded_representation = []
    file_index = 0
    isfile = True
    for e in disk:
        val = int(e)
        if isfile:
            for _ in range(val):
                expanded_representation.append(file_index)
            file_index += 1
        else:
            for _ in range(val):
                expanded_representation.append(-1)
        isfile = not isfile
    return expanded_representation


def swapper(er: list[int], debug=False) -> None:
    swap_end = len(er) - 1
    i = 0
    while i < len(er) - 1:
        if i >= swap_end:
            break
        if er[i] == -1:
            if er[swap_end] == -1:
                swap_end -= 1
            else:
                er[i] = er[swap_end]
                er[swap_end] = -1
                swap_end -= 1
                i += 1
                if debug:
                    print("".join([str(j) if j != -1 else "." for j in er]))
        else:
            i += 1


def file_swapper(disk: str, debug=False) -> list[int]:
    last_file = len(disk)//2
    shifts = {}
    files = {i: int(e) for i, e in enumerate(disk[::2])}
    spaces = {i: int(e) for i, e in enumerate(disk[1::2])}

    current_file = last_file
    while current_file > 0:
        for i in range(current_file):
            if spaces[i] >= files[current_file]:
                if i in shifts:
                    shifts[i].append(current_file)
                else:
                    shifts[i] = [current_file]
                spaces[i] -= files[current_file]
                spaces[current_file-1] += files[current_file]
                break
        current_file -= 1

    result = []
    files_already_added = set()
    for i in range(last_file):
        if i not in files_already_added:
            result.extend([i for _ in range(files[i])])
            files_already_added.add(i)
        if i in shifts:
            while shifts[i]:
                this_file = shifts[i].pop(0)
                result.extend([this_file for _ in range(files[this_file])])
                files_already_added.add(this_file)
        if i in spaces:
            result.extend([-1 for _ in range(spaces[i])])

    return result


def checksum(er: list[int]) -> int:
    result = sum([x * y for x, y in zip(er, range(len(er))) if x != -1])
    return result


def problem1(disk: str) -> int:
    er = represent_disk(disk)
    swapper(er)
    return checksum(er)


def problem2(disk: str) -> int:
    result = file_swapper(disk)
    return checksum(result)


def solve() -> None:
    file_path = pathlib.Path(__file__).absolute().parent / "data" / "day9" / "actual_inp.txt"  # noqa
    disk = data_loader(file_path)
    # print(problem1(disk))
    print(problem2(disk))
