"""bridge repair"""
from collections import namedtuple
from joblib import Parallel, delayed
from itertools import product
import operator
import pathlib
from typing import Callable

Instance = namedtuple("Instance", ["test_val", "remaining_nums"])


def concatenate_nums(a: int, b: int):
    return int(str(a)+str(b))


def data_loader(input_file: pathlib.Path) -> list[Instance]:
    dat = []
    with open(input_file, "r") as f:
        while row := f.readline():
            test_val, remaining_nums = row.split(":")
            dat.append(Instance(int(test_val), [int(i)
                       for i in remaining_nums.split()]))

    return dat


def checkone(operations_map: dict[str, Callable[[int, int], int]], instance: Instance) -> int:
    num_sol = 0
    num_possible_locations = len(instance[1]) - 1

    # dumbest solution: exhaustive search
    for operations in product(operations_map.keys(), repeat=num_possible_locations):
        if do_math(list(operations), instance.remaining_nums, operations_map) == instance.test_val:
            num_sol += 1

    return num_sol


def do_math(operations: list[str], numbers: list[int], operations_map: dict[str, Callable[[int, int], int]]) -> int:
    result = operations_map[operations.pop(0)](numbers[0], numbers[1])
    for i in range(2, len(numbers)):
        result = operations_map[operations.pop(0)](result, numbers[i])

    return result


def problem1(all_instances):
    operations_map = {"*": operator.mul, "+": operator.add}
    result = 0
    for instance in all_instances:
        num_sol = checkone(operations_map, instance)
        if num_sol > 0:
            result += instance.test_val
    return result


def problem2(all_instances):
    operations_map = {
        "*": operator.mul,
        "+": operator.add,
        "||": concatenate_nums
    }

    def checkone_wrapper(instance):
        if checkone(operations_map, instance):
            return instance.test_val
        return 0

    # about as legit as it gets lol
    results = Parallel(n_jobs=12)(delayed(checkone_wrapper)(instance)
                                  for instance in all_instances)

    final_result = sum(results)  # type: ignore
    return final_result


def solve() -> None:
    file_path = pathlib.Path(__file__).absolute().parent / "data" / "day7" / "actual_inp.txt"  # noqa

    all_instances = data_loader(file_path)

    print(problem1(all_instances))
    print(problem2(all_instances))
