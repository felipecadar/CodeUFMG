import networkx as nx
import random
import os

os.makedirs("input/", exist_ok=True)
os.makedirs("output/", exist_ok=True)

def genGraph(v, i, p=0.5):
    G=nx.gnp_random_graph(v,p,directed=True)

    DAG_bus = nx.DiGraph([(u,v,{'weight':random.randint(100,1000)}) for (u,v) in G.edges() if u<v])
    DAG_plane = nx.DiGraph([(u,v,{'weight':random.randint(100,1000)}) for (u,v) in G.edges() if u<v])

    with open(f"input/C_{i}", "w") as f:
        f.write(f"{v} {len(DAG_bus.edges) + len(DAG_plane.edges)}\n")
        for edge in DAG_bus.edges:
            u,v = edge
            w = DAG_bus[u][v]["weight"]
            f.write(f"{u+1} {v+1} 0 {w}\n")
        for edge in DAG_plane.edges:
            u,v = edge
            w = DAG_plane[u][v]["weight"]
            f.write(f"{u+1} {v+1} 1 {w}\n")

        bp = nx.dijkstra_path(DAG_bus, 0, v-1)
        pp = nx.dijkstra_path(DAG_plane, 0, v-1)

    with open(f"output/C_{i}", "w") as f:
        bus_w = sum([DAG_bus[bp[j]][bp[j+1]]['weight'] for j in range(len(bp)-1)])
        plane_w = sum([DAG_plane[pp[j]][pp[j+1]]['weight'] for j in range(len(pp)-1)])
        f.write(f"{min(bus_w, plane_w)}\n")

i = 0
for v in range(10, 101, 10):
    genGraph(v, i)
    i+=1

genGraph(100, i, p=1.0)
i+=1

