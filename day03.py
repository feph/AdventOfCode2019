from get_input import get_aoc_input
# inp = ["R8,U5,L5,D3",
        # "U7,R6,D4,L4"]
# inp = ["R75,D30,R83,U83,L12,D49,R71,U7,L72",
        # "U62,R66,U55,R34,D71,R55,D58,R83"]
# inp = ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
        # "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]
# inp = ["R2,U6", "U2, R6, U1,L1,D3"]
inp = get_aoc_input(3)

grid = {}
timings = {}
for w, wire in enumerate(inp):
    w = 1 << w
    t = 0
    x = 0
    y = 0
    steps = wire.split(",")
    for step in steps:
        step = step.strip()
        direction = step[0]
        num = int(step[1:])
        for i in range(1,num+1):
            t += 1
            if direction == "U":
                y += 1
            if direction == "D":
                y -= 1
            if direction == "R":
                x += 1
            if direction == "L":
                x -= 1
            grid[(x,y)] = grid.get((x,y),0) | w # set bit for "wire was here"
            if (w,x,y) not in timings.keys(): #only set first time
                timings[(w,x,y)] = t

distances = []
crossings = []
times = []
for k,v in grid.items():
    if v >= 3:
        crossings.append(k)
        distances.append(sum(map(abs,k)))

for c in crossings:
    ts = [timings[w,x,y] for w,x,y in timings.keys() if x == c[0] and y == c[1]]
    times.append(sum(ts))
print(f"crossings: {crossings}")
print(f"distances: {distances}")
print(f"times: {times}")
print(f"solution for part 1: {min(distances)}")
print(f"solution for part 2: {min(times)}")
