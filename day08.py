from get_input import get_aoc_input
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
inp = "".join(get_aoc_input(8))
ROWS = 6
COLS = 25

def chunk(l, n):
    i = 0
    while (i*n) < len(l):
        yield l[i*n:(i+1)*n]
        i += 1

layers = list(chunk(inp, ROWS*COLS))[::-1]
digits_zero = [layer.count("0") for layer in layers]
mz = min(digits_zero)
num_layer = digits_zero.index(mz)
res = layers[num_layer].count("1") * layers[num_layer].count("2")
print(f"checksum: {res}")

fig = plt.figure()
ax = plt.gca()
ax.set_facecolor('xkcd:salmon')
for layer in layers:
    layer = np.array([int(f) for f in layer])
    layer = layer.reshape(ROWS, COLS)
    bw = np.ma.masked_where(layer == 2, layer)
    plt.imshow(bw, cmap="gray", vmin=0, vmax=1, interpolation="none")
plt.show()
