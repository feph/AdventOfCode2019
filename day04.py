#from get_input import get_aoc_input
import itertools
import re
inp = "256310-732736"

min_pw, max_pw = map(int, inp.split("-"))
def double_digits(p):
    ds = [p[i] == p[i-1] for i in range(len(p))]
    return sum(ds) > 0

def check_pw(x):
    x = list(str(x))
    if double_digits(x):
        if x == sorted(x):
            return True
    return False

num_part1 = sum([check_pw(i) for i in range(min_pw,max_pw)])
print(f"solution for part 1: {num_part1}")

dd = re.compile(r'(?:^|(?<=(.)))(?!\1)(.)\2{1}(?!\2)') # match only exactly two following characters
def double_digits2(p):
    res = dd.search(p)
    return res

def check_pw2(x):
    x = str(x)
    if double_digits2(x):
        if list(x) == sorted(list(x)):
            return True
    return False

num_part2 = sum([check_pw2(i) for i in range(min_pw,max_pw)])
print(f"solution for part 2: {num_part2}")
