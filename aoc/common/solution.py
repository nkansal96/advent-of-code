import inspect
import os

from typing import Any, Dict, Tuple, Callable

SolutionFunction = Callable[[Any], Any]

SOLUTIONS: Dict[Tuple[int, int, bool], Callable[[str], Any]] = {}


def part_one(year: int, problem: int):
    return _solution(year, problem, part_two=False)


def part_two(year: int, problem: int):
    return _solution(year, problem, part_two=True)


def _solution(year: int, problem: int, part_two: bool):
    def wrapper(fn: SolutionFunction) -> SolutionFunction:
        # pre-execution checks on the validity of the function
        sig = inspect.signature(fn)
        key = (year, problem, part_two)
        try:
            assert key not in SOLUTIONS, f"Already registered a solution for {key}"
            assert len(sig.parameters) == 1, "Expected one parameter"
            k = list(sig.parameters.keys())[0]
            assert (
                sig.parameters[k].annotation is not inspect.Parameter.empty
            ), f"Expected `{k}` to have a type annotation"
        except AssertionError as e:
            raise AssertionError(f"validate({year}, {problem}, {fn.__name__})") from e

        def wrapped_fn(input_data: str) -> Any:
            dtype = sig.parameters[k].annotation
            return fn(dtype(input_data))

        SOLUTIONS[key] = wrapped_fn
        return fn

    return wrapper


def get(year: int, problem: int, part_two: bool) -> Callable[[str], Any]:
    fn = SOLUTIONS.get((year, problem, part_two))
    if fn is None:
        raise KeyError(
            f"No solution found for year={year}, problem={problem}, part_two={part_two}"
        )

    return fn


def generate(year: int, problem: int, name: str):
    curr_dir = os.path.dirname(__file__)
    dest_dir = os.path.abspath(os.path.join(curr_dir, "..", f"y{year}"))

    input_file = os.path.join(dest_dir, "input", f"{problem}.txt")
    py_file = os.path.join(dest_dir, f"p{problem}_{name}.py")

    for f in [input_file, py_file]:
        assert not os.path.isfile(f), f"Not generating because file exists: {f}"

    # create input file
    with open(input_file, "w"):
        print("created input file", input_file)

    # create code file
    with open(os.path.join(curr_dir, "solution.py.tpl"), "r") as tpl:
        with open(py_file, "w") as py:
            py.write(tpl.read().format(year=year, problem=problem))
        print("created source file", py_file)
