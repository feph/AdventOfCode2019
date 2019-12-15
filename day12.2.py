from get_input import get_aoc_input
import numpy as np
import re
import itertools
import sys

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
    perm = tuple(itertools.permutations(moon_idx, 2))
    axis_idx = range(0,3)
    moons = np.array([str2vec(v) for v in inp])
    start_moons = moons.copy()
    vels = np.array([np.zeros(3) for v in moons])
    start_vels = vels.copy()
    steps = np.zeros_like(axis_idx)
    # print(moons)
    # print(moons[:,0])
    # sys.exit(0)
    for ax in axis_idx:
        step = 0
        while True:
            step += 1
            for moon1_idx, moon2_idx in perm:
                pos1 = moons[moon1_idx][ax]
                pos2 = moons[moon2_idx][ax]
                if pos1 < pos2:
                    vels[moon1_idx][ax] += 1
                if pos1 > pos2:
                    vels[moon1_idx][ax] -= 1
            for mi in moon_idx:
                moons[mi] += vels[mi]
            if np.allclose(moons[:,ax], start_moons[:,ax]) and np.allclose(vels[:,ax], start_vels[:,ax]):
                break
            if step % 1000 == 0:
                print(step)
                sys.stdout.flush()
        steps[ax] = step
        print(f"{step} reps for axis {ax}")
            # if step % 1 == 0:
        #     print(f"after step {step}:")
        #     for m,v in zip(moons,vels):
        #         pot = abs(m).sum()
        #         kin = abs(v).sum()
        #         print(f"pos={m}, vel={v}, pot={pot}, kin={kin}, tot={kin*pot}")
        #     print((abs(moons).sum(axis=1)*abs(vels).sum(axis=1)).sum())


        # if step == 4:
            # break
    loop = np.lcm.reduce(steps)
    print(f"repeated start state after {loop} steps.")

