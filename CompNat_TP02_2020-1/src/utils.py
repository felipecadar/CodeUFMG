import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def visualize(g, t):
    G = nx.from_numpy_matrix(g)
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, width=1.0, edge_cmap=plt.cm.Blues)
    plt.show()

def genEnv(filename):

    raw = np.loadtxt(filename, delimiter="\t", dtype=np.int)
    raw[:, :2] -= 1

    n = len(np.unique(raw[:, :2]))

    g = np.zeros([n,n], dtype=np.int8)
    t = np.ones([n,n], dtype=np.float)

    for edge in raw:
        g[edge[0], edge[1]] = edge[2]

    return g, t

def updateT(t, evap):
    t = t * (1-evap)


def getInitalNodes(g):
    safe_init = np.sum(g, axis=1)
    return np.where(safe_init > 0)[0]