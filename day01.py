import logging
from get_input import get_aoc_input
from math import floor
modules = get_aoc_input(day=1)


### Part 1
fuel = sum([floor(int(mass) / 3) - 2 for mass in modules])
print(f'Needed fuel: {fuel}')

### Part 2

def fuel4mass(x):
    return floor(int(x) / 3) - 2

def fuel4module(m):
    fuel = fuel4mass(m)
    fuels = []
    while fuel > 0:
        fuels.append(fuel)
        fuel = fuel4mass(fuel)
    return sum(fuels)

#print(fuel4module(14))
#print(fuel4module(1969))

total_fuel = sum([fuel4module(m) for m in modules])
print(f'Total fuel for part 2: {total_fuel}')
