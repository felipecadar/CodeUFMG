import numpy as np
import argparse
import os, sys, uuid
import glob
import time

from tools import *
from algoritmos import startSearchDFS, startSearchBFS, startSearchIDS, startSearchAStar

import errno
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python ≥ 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def parseArgs():
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument("-a", "--algoritmo", type=str, default="BFS",
                        choices=["dfs", "bfs", "ids", "a_star"], help="Algoritmo de busca")
    parser.add_argument("-i", "--input", type=str,
                        default="maps/input1.txt", help="Mapa de entrada")
    parser.add_argument("-o", "--output", type=str,
                        default="output/", help="Diretorio de saida")
    parser.add_argument("-id", "--id", type=str,
                        default="", help="ID da execução")
    parser.add_argument("-w", "--W", type=int,
                        default=0, help="ID da execução")
    parser.add_argument("-v", "--verbose", type=int, choices=[-1,0,1,2,3,4],
                        default=-1, help="Print all info - Verbose 4 needs OpenCV and Matplotlib")
    parser.add_argument("-t", "--time", action="store_true", default=False, help="Time it")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    os.environ["TP_DEBUG"] = str(args.verbose)

    input_map_path = args.input
    if not os.path.isfile(input_map_path):
        fail("Fail to open %s" % input_map_path)
        exit()

    start_time = time.time()
    char_map, W = loadMap(input_map_path)
    end_time = time.time()
    # displayMap(char_map)

    if args.W > 0: # W overwrite 
        W = args.W

    start_time = time.time()
    if args.algoritmo == "dfs":
        status, path = startSearchDFS(char_map, W)
    elif args.algoritmo == "dfs":
        status, path = startSearchBFS(char_map, W)
    elif args.algoritmo == "ids":
        status, path = startSearchIDS(char_map, W)
    elif args.algoritmo == "a_star":
        status, path = startSearchAStar(char_map, W)
    end_time = time.time()

    if args.time:
        print(end_time-start_time)
        exit()

    confirm(str(status))
    if args.verbose == 4:
        import cv2
        img = displayPath(char_map, path, 1)
        cv2.imwrite("{}_{}.png".format(args.algoritmo, input_map_path.split("/")[-1].replace(".txt","")), img)


    if status:
        checkpoints = 0
        for m in path:
            if char_map[m] == ord("#"):
                checkpoints += 1

        print(len(path),checkpoints,path[0])