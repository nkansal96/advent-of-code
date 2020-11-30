#! /usr/bin/env python

import argparse
import os
import timeit

import aoc.common.solution


def get_args():
    parser = argparse.ArgumentParser(description="Run Advent of Code solutions")
    parser.add_argument(
        "-y", "--year", help="Advent year (e.g. 2020)", required=True, type=int
    )
    parser.add_argument(
        "-p", "--problem", help="Problem number (e.g. 3)", required=True, type=int
    )
    parser.add_argument(
        "-t",
        "--part_two",
        help="Run part two of the given problem number",
        action="store_true",
    )
    parser.add_argument(
        "-g",
        "--generate",
        help="Create the boilerplate for a solution",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Literal input to pass to the solution",
    )
    parser.add_argument(
        "-f",
        "--input_file",
        help="A file to read as input to the solution",
    )
    parser.add_argument(
        "-r",
        "--profile",
        help="Profile the execution of the solution with the given number of iterations",
        type=int,
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    if args.generate:
        aoc.common.solution.generate(args.year, args.problem, args.generate)
        exit(0)

    if args.input is not None and args.input_file is not None:
        raise ValueError("Must provide only one of --input or --input_file")

    input_data = args.input
    input_file = args.input_file

    if input_file is None and input_data is None:
        input_file = os.path.join(
            os.path.dirname(__file__),
            "aoc",
            f"y{args.year}",
            "input",
            f"{args.problem}.txt",
        )

    if input_file is not None:
        with open(input_file, "r") as f:
            input_data = f.read().strip()

    solution = aoc.common.solution.get(args.year, args.problem, args.part_two)

    if args.profile:
        print(
            args.profile,
            "runs in",
            timeit.timeit(
                stmt="solution(input_data)", number=args.profile, globals=globals()
            ),
            "seconds",
        )
    else:
        ans = solution(input_data)
        if ans is not None:
            print("Solution:", ans)
