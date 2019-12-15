from get_input import get_aoc_input
import numpy as np
import re
import itertools

reg = re.compile(r'<x=[ ]*([+-]?\d+)\s*,\s*y=\s*([+-]?\d+)\s*,\s*z\s*=\s*([+-]?\d+)>')
def str2vec(s):
    m = reg.search(s)
    return np.array([float(m.group(i)) for i in range(1,4)])

def vec2str(v):
    return f"<x={v[0]:>4}, y={v[1]:>4}, z={v[2]:>4}>"

if __name__ == "__main__":

    inp = """<x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>""".split("\n")

    inp = get_aoc_input(12)

    moon_idx = range(0,4)
    axis_idx = range(0,3)
    moons = np.array([str2vec(v) for v in inp])
    vels = np.array([np.zeros(3) for v in moons])
    for step in range(1,1001):
        for moon1_idx, moon2_idx in itertools.permutations(moon_idx, 2):
            for axis in axis_idx:
                pos1 = moons[moon1_idx][axis] 
                pos2 = moons[moon2_idx][axis]
                if pos1 < pos2:
                    vels[moon1_idx][axis] += 1
                if pos1 > pos2:
                    vels[moon1_idx][axis] -= 1
        for mi in moon_idx:
            moons[mi] += vels[mi]
        if step % 10 == 0:
            print(f"after step {step}:")
            for m,v in zip(moons,vels):
                pot = abs(m).sum()
                kin = abs(v).sum()
                print(f"pos={m}, vel={v}, pot={pot}, kin={kin}, tot={kin*pot}")
            print((abs(moons).sum(axis=1)*abs(vels).sum(axis=1)).sum())


