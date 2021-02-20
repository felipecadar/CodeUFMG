import subprocess
import multiprocessing
import os
import glob
import sys
import matplotlib.pyplot as plt
import matplotlib
import shlex
import tqdm
import numpy as np
import pickle

from tools import mkdir_p

def chunker_list(seq, size):
    return list(seq[i::size] for i in range(size))


# MAKE_EXPS = False
MAKE_EXPS = True

MAKE_GRAPHS = False
# MAKE_GRAPHS = True

MAKE_FINAL_EXPS = False
# MAKE_FINAL_EXPS = True

MAKE_FINAL_GRAPHS = False
# MAKE_FINAL_GRAPHS = True

parallel = 12

maps = sorted(glob.glob("maps/input*"))

alpha = [0.1, 0.3, 0.5, 0.7, 0.9]
exploration = [0.1, 0.3, 0.5, 0.7, 0.9]
discount = [0.1, 0.3, 0.5, 0.7, 0.9]
REP = 10

variables = {
    "alpha": alpha,
    "exploration": exploration,
    "discount": discount,
}

if MAKE_EXPS:
    args = []
    for exp_name in variables:
        done = 0
        missing = 0
        for map_path in maps:
            for var in alpha:
                for i in range(REP):
                    map_name = map_path.split("/")[-1].split(".")[0]
                    exp_id = "exp_{}_{}_{}_{}".format(map_name, exp_name, var, i)
                    if not os.path.isfile(os.path.join("logs", exp_id, "qtable.pkl")):
                        missing += 1
                    else:
                        done += 1
        print(exp_name, "done", done, "missing", missing)