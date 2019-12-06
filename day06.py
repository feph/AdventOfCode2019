from get_input import get_aoc_input
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
plt.ion()

testcase = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""".split("\n")

elist = [tuple(line.split(")")) for line in testcase]
print(elist)
G = nx.Graph()
G.add_edges_from(elist)

nx.draw_networkx(G)

distances = [len(nx.shortest_path(G, source='COM',target=a))-1 for a in G.nodes()]

print(sum(distances))

aoc_input = get_aoc_input(6)
elist = [tuple(line.split(")")) for line in aoc_input]
# print(elist)
G = nx.Graph()
G.add_edges_from(elist)

# nx.draw_networkx(G)
# plt.waitforbuttonpress()
distances = [len(nx.shortest_path(G, source='COM',target=a))-1 for a in G.nodes()]
print(sum(distances))

path = len(nx.shortest_path(G, source='YOU',target='SAN')) -3
print(path)
