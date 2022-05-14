import networkx as nx
import random
import os

os.makedirs("input/", exist_ok=True)
os.makedirs("output/", exist_ok=True)

def randomGraph(i, vertices, e = None):
    if(not e):
        e = random.randint(vertices, (vertices*(vertices-1))/2)
    g = nx.gnm_random_graph(vertices, e)
    for _, _, w in g.edges(data=True):
        w['weight'] = random.randint(10,100)

    with open(f'input/C_{i}', 'w') as f:
        f.write(f'{vertices} {e}\n')
        for u, v, w in g.edges(data=True):
            f.write(f'{u+1} {v+1} {w["weight"]}\n')

    T = nx.minimum_spanning_tree(g)
    total = sum([w["weight"] for _, _, w in T.edges(data=True)])

    with open(f'output/C_{i}', 'w') as f:
        f.write(f"{total}\n")
        

cases = 0
randomGraph(cases, 10, 15)
cases+=1

for v in range(0, 50, 10):
    randomGraph(cases, v)
    cases+= 1

for v in range(50, 1001, 100):
    randomGraph(cases, v)
    cases+= 1

randomGraph(cases, 1000, int((1000*(1000-1))) / 2)