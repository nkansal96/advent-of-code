Solutions to the Advent of Code challenge.

You can view each solution under `aoc/y{year}/p{problem}_*.py`.

The respective inputs in are `aoc/y{year}/inputs/{problem}.txt`.

This repo uses Python 3.8.

There is a main script that can run individual solutions and parts:

```
$ ./scripts/setup.sh
$ source .env/bin/activate
$ pip install -r requirements.txt
$ ./main.py --help
usage: main.py [-h] -y YEAR -p PROBLEM [-t] [-g GENERATE] [-i INPUT]
               [-f INPUT_FILE] [-r PROFILE]

Run Advent of Code solutions

optional arguments:
  -h, --help            show this help message and exit
  -y YEAR, --year YEAR  Advent year (e.g. 2020)
  -p PROBLEM, --problem PROBLEM
                        Problem number (e.g. 3)
  -t, --part_two        Run part two of the given problem number
  -g GENERATE, --generate GENERATE
                        Create the boilerplate for a solution
  -i INPUT, --input INPUT
                        Literal input to pass to the solution
  -f INPUT_FILE, --input_file INPUT_FILE
                        A file to read as input to the solution
  -r PROFILE, --profile PROFILE
                        Profile the execution of the solution with the given
                        number of iterations
```
