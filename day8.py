from collections import defaultdict
from itertools import combinations
import pathlib


def data_loader(input_file: pathlib.Path) -> list[list[str]]:
    grid = []
    with open(input_file, "r") as f:
        while row := f.readline():
            grid.append(list(row.split()[0]))

    return grid


def print_grid(grid: list[list[str]]) -> None:
    prnt_str = []
    for i in range(len(grid)):
        prnt_str.append("".join(grid[i]))
    print("\n".join(prnt_str))


def parse_grid(grid: list[list[str]]):
    antenna = defaultdict(lambda: set())
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != ".":
                antenna[grid[i][j]].add((i, j))

    return antenna


def manhattan_histance(loc1: tuple[int, int], loc2: tuple[int, int]) -> tuple[int, int]:
    return loc1[0] - loc2[0], loc1[1] - loc2[1]


def find_antinodes(grid: list[list[str]], resonance: bool = False) -> set[int]:
    antenna = parse_grid(grid)
    antinodes = set()
    grid_limits = (len(grid), len(grid[0]))

    for antenna_type in antenna:
        if len(antenna[antenna_type]) == 1:
            continue

        for antenna1, antenna2 in combinations(antenna[antenna_type], 2):
            if resonance:
                antinodes.add(antenna1)
                antinodes.add(antenna2)

            md = manhattan_histance(antenna1, antenna2)
            n = 1
            while True:
                additions = 0
                new_loc1 = antenna1[0] + n*md[0], antenna1[1] + n*md[1]
                new_loc2 = antenna2[0] - n*md[0], antenna2[1] - n*md[1]

                if 0 <= new_loc1[0] < grid_limits[0] and 0 <= new_loc1[1] < grid_limits[1]:
                    antinodes.add(new_loc1)
                    additions += 1
                if 0 <= new_loc2[0] < grid_limits[0] and 0 <= new_loc2[1] < grid_limits[1]:
                    antinodes.add(new_loc2)
                    additions += 1
                if not resonance or additions == 0:
                    break

                n += 1
    return antinodes


def problem1(grid: list[list[str]]) -> int:
    return len(find_antinodes(grid, resonance=False))


def problem2(grid: list[list[str]]) -> int:
    return len(find_antinodes(grid, resonance=True))


def solve() -> None:
    file_path = pathlib.Path(__file__).absolute().parent / "data" / "day8" / "actual_inp.txt"  # noqa
    grid = data_loader(file_path)
    print("Problem1:", problem1(grid))
    print("Problem2:", problem2(grid))
