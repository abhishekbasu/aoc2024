from collections import Counter
import pathlib


def data_loader(input_file: pathlib.Path) -> tuple[list[int], list[int]]:
    arr1 = []
    arr2 = []
    with open(input_file, "r") as f:
        while row := f.readline():
            elem1, elem2 = row.split()
            arr1.append(int(elem1))
            arr2.append(int(elem2))
    return arr1, arr2


def total_distance(arr1: list[int], arr2: list[int]) -> int:
    _arr1 = sorted(arr1)
    _arr2 = sorted(arr2)
    distance = sum([abs(_arr1[i] - _arr2[i]) for i in range(len(_arr1))])
    return distance


def find_similarity(arr1: list[int], arr2: list[int]) -> int:
    _ct2 = Counter(arr2)
    similarity = 0
    for k in arr1:
        similarity += k*_ct2[k]

    return similarity


def solve() -> None:
    file_path = pathlib.Path(__file__).absolute().parent / "data" / "day1" / "actual_inp.txt"  # noqa
    arr1, arr2 = data_loader(file_path)
    distance = total_distance(arr1, arr2)
    similarity = find_similarity(arr1, arr2)

    print("Distance", distance)
    print("Similarity", similarity)
