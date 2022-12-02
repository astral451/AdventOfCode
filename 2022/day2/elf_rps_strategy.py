
# For this to work be sure to add AOC_SESSION environment variable with the cookie session_id
from aocd.models import Puzzle



if __name__ == "__main__":
    puzzle = Puzzle(year=2022,day=2)
    print(puzzle)