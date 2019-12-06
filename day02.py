from get_input import get_aoc_input
import itertools

inp = get_aoc_input(2)
#inp = "1,9,10,3,2,3,11,0,99,30,40,50"
code = (''.join(inp)).split(',')

codes = list(map(int, code))

## part 1
codes1 = list(codes)
noun = 12
verb = 2
codes1[1] = noun
codes1[2] = verb

def run_program(codes_inp):
    codes = list(codes_inp) # new memory
    ip = 0
    while True:
        c = codes[ip]
        dest = codes[ip+3]
        if c == 1:
            codes[dest] = codes[codes[ip+1]] + codes[codes[ip+2]]
        if c == 2:
            codes[dest] = codes[codes[ip+1]] * codes[codes[ip+2]]
        if c == 99:
            break
        ip += 4
    return codes

part1 = run_program(codes)
print(f'Solution for part 1: {part1[0]}')

## part 2
nouns = range(0,99)
verbs = range(0,99)
for noun, verb in itertools.product(nouns, verbs):
    codes2 = list(codes)
    codes2[1] = noun
    codes2[2] = verb
    res = run_program(codes2)

    if res[0] == 19690720:
        solution = 100 * noun + verb

print(f'solution for part 2: {solution}')
