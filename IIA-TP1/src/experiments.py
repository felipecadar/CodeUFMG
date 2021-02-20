import subprocess
import multiprocessing
import os, glob, sys
import matplotlib.pyplot as plt
import matplotlib
import shlex
import tqdm
import numpy as np
import pickle

GEN_IMAGES = True
BARS = False

maps = sorted(glob.glob("maps/input*"))
algoritmos = ["DFS","BFS","IDS","A*"]
Ws = list(range(0, 100)) + [10000000]
REP = 30



if GEN_IMAGES:
    for map_path in maps:
        for alg in algoritmos:    
            cmd = "python3 src/main.py --input {} --algoritmo {} -v 4".format(map_path, alg)
            cmd = shlex.split(cmd)
            p = subprocess.Popen(cmd,stdout = subprocess.PIPE, stderr= subprocess.PIPE)
            p.wait()

    for map_path in maps:
        for alg in algoritmos[2:]:    
            cmd = "python3 src/main.py --input {} --algoritmo {} -v 4 -W 10000".format(map_path, alg)
            cmd = shlex.split(cmd)
            p = subprocess.Popen(cmd,stdout = subprocess.PIPE, stderr= subprocess.PIPE)
            p.wait()
    exit()

def run(args):
    cmd, map_path, alg, w = args 
    cmd = shlex.split(cmd)
    p = subprocess.Popen(cmd,stdout = subprocess.PIPE, stderr= subprocess.PIPE)
    p.wait()
    output,error = p.communicate()
    return (map_path, alg, w, float(output.decode("utf-8") .strip()))

if os.path.isfile("exp_results.pkl"):
    times = pickle.load(open("exp_results.pkl", "rb"))
else:
    W = 0
    pool = multiprocessing.Pool(os.cpu_count())
    times = {}
    args = []
    for map_path in maps:
        for alg in algoritmos:
            for i in range(REP):
                cmd = "python3 src/main.py --input {} --algoritmo {} --W {} -t".format(map_path, alg, W)
                args.append((cmd, map_path, alg, W))

    # Extra inputs
    W = 100000
    for map_path in maps:
        for alg in algoritmos[2:]:
            for i in range(REP):
                cmd = "python3 src/main.py --input {} --algoritmo {} --W {} -t".format(map_path, alg, W)
                args.append((cmd, map_path, alg, W))

    for alg in algoritmos[0:2]:
        for i in range(REP):
            cmd = "python3 src/main.py --input {} --algoritmo {} --W {} -t".format(maps[0], alg, W)
            args.append((cmd, maps[0], alg, W))

    with tqdm.tqdm(total=len(args)) as pbar:
        for i,res in enumerate(pool.imap_unordered(run, args)):
            map_path, alg, w, t = res
            if not alg in times:
                times[alg] = {}

            if not map_path in times[alg]:
                times[alg][map_path] = {}

            if not w in times[alg][map_path]:
                times[alg][map_path][w] = []

            times[alg][map_path][w].append(t)
            pbar.update()

    pickle.dump(times, open("exp_results.pkl", "wb"))



x = np.arange(len(algoritmos))  # the label locations
x2 = np.arange(len(algoritmos))[2:]  # the label locations
width = 0.35  # the width of the bars
W = 100000

if BARS:
    fig, axes = plt.subplots(1, 3, figsize=[14, 5])
    for idx, ax in enumerate(axes):
        map_path = maps[idx]

        if (idx == 0):
            y1 = [np.mean(times[alg][map_path][0]) for alg in  algoritmos]
            rects1 = ax.bar(x - width/2, y1, width, label='W Baixo')

            y2 = [np.mean(times[alg][map_path][W]) for alg in  algoritmos]
            rects2 = ax.bar(x + width/2, y2, width, label='W Alto')
        else:
            y1 = [np.mean(times[alg][map_path][0]) for alg in  algoritmos]
            rects1 = ax.bar(x - width/2, y1, width, label='W Baixo')

            y2 = [np.mean(times[alg][map_path][W]) for alg in  algoritmos[2:]]
            rects2 = ax.bar(x2 + width/2, y2, width, label='W Alto')


        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Média do tempo em segundos')
        ax.set_title('Teste no mapa {}'.format(map_path.split("/")[-1]))
        ax.set_xticks(x)
        ax.set_xticklabels(algoritmos)
        ax.legend()


        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')


        # autolabel(rects1)
        # autolabel(rects2)

    fig.tight_layout()
    plt.savefig("imgs/bars.png")
