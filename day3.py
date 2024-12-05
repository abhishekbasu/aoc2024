"""Regex shenanigans begin."""
import math
import pathlib
import re


MUL_PATTERN = r"mul\(\d+,\d+\)"
DO_PATTERN = r"do\(\)"
DONT_PATTERN = r"don't\(\)"


def data_loader(input_file: pathlib.Path) -> str:
    dat = ""
    with open(input_file, "r") as f:
        dat = f.read()
    return dat


def find_match_loc(input_str: str, pattern: str) -> list[tuple[int, int]]:
    match_locs = [
        (match.start(0), match.end(0)) for match in re.finditer(pattern, input_str)
    ]
    return match_locs


def perform_mul(mul_instance: str) -> int:
    return math.prod(map(lambda x: int(x), mul_instance[4:-1].split(",")))


def problem1(input_str: str) -> int:
    mul_matches = find_match_loc(input_str, MUL_PATTERN)
    total = 0
    for match in mul_matches:
        total += perform_mul(input_str[match[0]: match[1]])

    return total


def problem2(input_str: str) -> int:
    mul_matches = find_match_loc(input_str, MUL_PATTERN)
    do_matches = find_match_loc(input_str, DO_PATTERN)
    dont_matches = find_match_loc(input_str, DONT_PATTERN)

    all_matches = {match[0]: ("mul", match) for match in mul_matches}
    all_matches |= {match[0]: ("do", match) for match in do_matches}
    all_matches |= {match[0]: ("dont", match) for match in dont_matches}

    valid = True
    total = 0

    for k in sorted(all_matches.keys()):
        if all_matches[k][0] == "mul":
            if valid:
                total += perform_mul(
                    input_str[all_matches[k][1][0]: all_matches[k][1][1]]
                )
        elif all_matches[k][0] == "do":
            valid = True
        elif all_matches[k][0] == "dont":
            valid = False
        else:
            raise ValueError(f"Unknown key {all_matches[k][0]}.")

    return total


def solve() -> None:
    file_path = pathlib.Path(__file__).absolute().parent / "data" / "day3" / "actual_inp.txt"  # noqa

    dat = data_loader(file_path)
    print(problem1(dat))
    print(problem2(dat))
