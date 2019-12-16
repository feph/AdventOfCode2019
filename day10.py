from get_input import get_aoc_input
from itertools import product
import numpy as np
import math
aoc_inp = get_aoc_input(10)

#inp = """.#..#
#.....
######
#....#
#...##"""

inp = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

inp = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

inp = "\n".join(aoc_inp)

inp=inp.strip()

w = inp.index('\n')
# print(w)
h = int((len(inp)-inp.count('\n'))/(w))
# print(h)
grid = [list(l) for l in inp.split('\n')]

grid = list(map(list, zip(*grid))) #swap indices
# print(grid)
# assert grid[1][0] == '#'

asteroids = []
for x, p in enumerate(grid):
    for y, f in enumerate(p):
        if f == '#':
            asteroids.append((x,y))

# print(asteroids)

start = (2,2)
def get_radius(start, asteroids, radius, w, h):
    xs,ys = start
    left = [(xs-radius, y) for y in range(ys-radius, ys+radius)
            if y < h and y >= 0 and xs-radius >= 0 and xs-radius < w]
    bottom= [(x, ys+radius) for x in range(xs-radius, xs+radius)
             if ys+radius < h and ys+radius >= 0 and x >= 0 and x < w]
    right= [(xs+radius, y) for y in range(ys-radius+1, ys+radius+1)
            if y < h and y >= 0 and xs+radius > 0 and xs+radius< w]
    upper = [(x, ys-radius) for x in range(xs-radius+1, xs+radius+1)
             if ys-radius < h and ys-radius >= 0 and x >= 0 and x < w] 
    return [a for a in asteroids if a in left or a in bottom or a in right or a in upper]
    # print(left)
# print(bottom)
# print(right)
# print(upper)
def blocked_by(blockers, new_point, viewpoint):
    for blocker in blockers:
        v1 = (blocker[0] - viewpoint[0], blocker[1] - viewpoint[1])
        v2 = (new_point[0] - viewpoint[0], new_point[1] - viewpoint[1])
        if v1[0]*v2[1]-v1[1]*v2[0] == 0:
            dot = v1[0]*v2[0]+v1[1]*v2[1]
            if dot > 0:
                # print(f"blocked by {blocker}!")
                # print(f"dot prod: {dot}")
                # print(f"v1: {v1}")
                # print(f"v2: {v2}")
                # print(f"{new_point} not visible from {viewpoint}!")
                return True
    return False

visible = {}
for asteroid in asteroids:
    visible[asteroid] = get_radius(asteroid, asteroids, 1, w, h)
    # print(f"visible from {asteroid} in radius 1: {visible[asteroid]}")
    left = asteroid[0]
    right = w - left - 1
    top = asteroid[1]
    bottom = h - top -1
    max_radius = max(left, right, top, bottom)
    for radius in range(2, max_radius+1):
        candidates = get_radius(asteroid, asteroids, radius, w, h)
        # print(f"candidates with radius = {radius}: {candidates}")
        new_objects = [c for c in candidates if not blocked_by(visible[asteroid], c, asteroid)]
        # print(new_objects)
        if new_objects:
            visible[asteroid] += new_objects
    # print(f"total visible asteroids from {asteroid}: {len(visible[asteroid])}")

max_vis = max(visible.keys(), key=lambda x: len(visible[x]))
print(f"maximum visible: {len(visible[max_vis])} for {max_vis})")


#### part 2
vapor_counter = 0
station = max_vis
visible = visible[max_vis]
print(f"station at {station}")
def calculate_angle(station, ast):
    x = ast[0] - station[0]
    y = ast[1] - station[1]
    theta = np.degrees(math.atan2(y,x)) + 90
    if ast == (11,12):
        print(theta)
    if theta < 0:
        theta += 360
    return theta
angles =  {}
for v in visible:
    angles[v] = calculate_angle(station,v)
angles_idx_sorted = sorted(angles, key=lambda x: angles[x])
i = 199
print(f"{i+1}.")
min_angle_idx = angles_idx_sorted[i]
print(angles[min_angle_idx])
print(min_angle_idx)

# print(f"{v} visible from {station}, diff: {(v[0]-station[0], v[1]-station[1])} angle: {t:.2f}")


# def vaporize(coord):
#     del asteroids[coord]
#     vapor_counter += 1

# vec = (0, -1)
# angles = {}
# for asteroid in visible:
#     angle = calculate_angle(vec, asteroid) # ccw angle, always positive
#     angles[asteroid] = angle
#     if angle == 0:
#         vaporize(asteroid)
#         break

# smallest_angle = min(angles.keys(), key=lambda x: angles[x])
# new_vec = asteroids[smallest_angle]
# if ticks:over(new_vec):
#     visible = get_visible_from(station)
