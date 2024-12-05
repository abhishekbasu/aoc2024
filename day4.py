from collections import defaultdict
import pathlib


def data_loader(input_file: pathlib.Path) -> list[list[str]]:
    dat = []
    with open(input_file, "r") as f:
        while row := f.readline():
            dat.append(list(row.split()[0]))

    return dat


def print_all(str_mat: list[list[str]]) -> None:
    """Check if the data has loaded properly."""
    for i in range(len(str_mat)):
        for j in range(len(str_mat[0])):
            print(f"{str_mat[i][j]}({i}, {j})", end=",")
        print("\n")


def create_patterns(word: str) -> dict[str, dict[tuple[int, int], str]]:
    """Generate patterns we need to exhaustively look for."""
    origin = (0, 0)
    letters = list(word)
    grad = {
        "south": (1, 0),
        "north": (-1, 0),
        "east": (0, 1),
        "west": (0, -1),
        "south-east": (1, 1),
        "south-west": (1, -1),
        "north-east": (-1, 1),
        "north-west": (-1, -1)
    }

    patterns = {}

    for direction in grad:
        patterns[direction] = {}
        for i, letter in enumerate(letters):
            patterns[direction][
                (origin[0] + i*grad[direction][0],
                 origin[1] + i*grad[direction][1])
            ] = letter

    return patterns


def pattern_checker(
    pattern: dict[tuple[int, int], str],
    str_mat: list[list[str]],
    start_pos: tuple[int, int]
) -> bool:
    limit_x = len(str_mat[0])
    limit_y = len(str_mat)

    for delta in pattern:
        loc_y = start_pos[0] + delta[0]
        loc_x = start_pos[1] + delta[1]

        if loc_x < 0 or loc_y < 0:
            return False

        if loc_x >= limit_x or loc_y >= limit_y:
            return False

        if str_mat[loc_y][loc_x] != pattern[delta]:
            return False
    return True


def problem1(
    patterns: dict[str, dict[tuple[int, int], str]],
    str_mat: list[list[str]],
    *,
    debug=False
) -> int:
    total_xmas = 0
    for i in range(len(str_mat)):
        for j in range(len(str_mat[0])):
            start_pos = (i, j)
            for k, pattern in patterns.items():
                if pattern_checker(pattern, str_mat, start_pos):
                    total_xmas += 1
                    if debug:
                        print(f"pattern_name={k}, {start_pos=}")
    return total_xmas


def problem2(
    patterns: dict[str, dict[tuple[int, int], str]],
    str_mat: list[list[str]],
) -> int:
    total_xmas = 0
    results = defaultdict(lambda: 0)
    for i in range(len(str_mat)):
        for j in range(len(str_mat[0])):
            start_pos = (i, j)
            for k, pattern in patterns.items():
                if pattern_checker(pattern, str_mat, start_pos):

                    a_offset = [w for w, x in pattern.items() if x == "A"][0]
                    results[(start_pos[0]+a_offset[0],
                             start_pos[1]+a_offset[1])] += 1

    for k in results:
        if results[k] >= 2:
            total_xmas += 1
    return total_xmas


def solve() -> None:
    file_path = pathlib.Path(__file__).absolute().parent / "data" / "day4" / "actual_inp.txt"  # noqa
    patterns1 = create_patterns("XMAS")
    str_mat = data_loader(file_path)
    print(problem1(patterns1, str_mat))

    patterns2 = create_patterns("MAS")
    patterns2 = {k: v for k, v in patterns2.items() if "-" in k}

    print(problem2(patterns2, str_mat))
