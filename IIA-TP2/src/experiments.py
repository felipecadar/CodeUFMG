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

MAKE_EXPS = False
MAKE_GRAPHS = False
MAKE_FINAL_EXPS = False
MAKE_FINAL_GRAPHS = False




# MAKE_EXPS = True
# MAKE_GRAPHS = True
# MAKE_FINAL_EXPS = True
MAKE_FINAL_GRAPHS = True

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
    exp_name = "alpha"
    for map_path in maps:
        for var in alpha:
            for i in range(REP):
                map_name = map_path.split("/")[-1].split(".")[0]
                exp_id = "exp_{}_{}_{}_{}".format(map_name, exp_name, var, i)
                if not os.path.isfile(os.path.join("logs", exp_id, "qtable.pkl")):
                    cmd = "python3 src/main.py --input {} -lr {} -id  {} -s".format(
                        map_path, var, exp_id)
                    args.append(cmd)

    exp_name = "exploration"
    for map_path in maps:
        for var in exploration:
            for i in range(REP):
                map_name = map_path.split("/")[-1].split(".")[0]
                exp_id = "exp_{}_{}_{}_{}".format(map_name, exp_name, var, i)
                if not os.path.isfile(os.path.join("logs", exp_id, "qtable.pkl")):
                    cmd = "python3 src/main.py --input {} -e {} -id  {} -s".format(
                        map_path, var, exp_id)
                    args.append(cmd)

    exp_name = "discount"
    for map_path in maps:
        for var in discount:
            for i in range(REP):
                map_name = map_path.split("/")[-1].split(".")[0]
                exp_id = "exp_{}_{}_{}_{}".format(map_name, exp_name, var, i)
                if not os.path.isfile(os.path.join("logs", exp_id, "qtable.pkl")):
                    cmd = "python3 src/main.py --input {} -y {} -id  {} -s".format(
                        map_path, var, exp_id)
                    args.append(cmd)

    parallel_args = chunker_list(args, parallel)
    files = [open("%i.sh" % i, 'w') for i in range(parallel)]
    final_file = open("run_all.sh", 'w')
    for i in range(parallel):
        for cmd in parallel_args[i]:
            files[i].write(cmd + " -t " + str(i) + "\n")

        files[i].close()
        final_file.write("sh %i.sh & " % i)
    final_file.close()


CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


final_params = {
    "input0": {},
    "input1": {},
    "input2": {},
    "input3": {},
    "input4": {},
    "input5": {},
    "input6": {},
    "input7": {},
}


def integrate(y_vals, h):
    i = 1
    total = y_vals[0] + y_vals[-1]
    for y in y_vals[1:-1]:
        if i % 2 == 0:
            total += 2 * y
        else:
            total += 4 * y
        i += 1
    return total * (h / 3.0)


if MAKE_GRAPHS:
    mkdir_p("graphs")
    for exp_name, params in variables.items():
        for map_path in maps:
            best_val = None
            best_param = None

            for idx, var in enumerate(params):
                rewards = []
                for i in range(REP):
                    map_name = map_path.split("/")[-1].split(".")[0]
                    exp_id = "exp_{}_{}_{}_{}".format(
                        map_name, exp_name, var, i)

                    info = pickle.load(
                        open(os.path.join("logs", exp_id, "log.pkl"), "rb"))
                    rewards.append(info["metrics"])

                rewards = np.array(rewards)
                area = integrate(np.mean(rewards, axis=0), 1)
                if best_val == None or area > best_val:
                    best_val = area
                    best_param = var

                plt.plot(moving_average(np.mean(rewards, axis=0), 15),
                         color=CB_color_cycle[idx], label=str(var))

            final_params[map_name][exp_name] = best_param

            plt.title("Cumulative Rewards {} - {}".format(exp_name, map_name))
            plt.legend(title=exp_name, loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=len(params))
            plt.tight_layout()
            plt.savefig("graphs/{}-{}.png".format(map_name, exp_name), dpi=200)
            plt.close()
    pickle.dump(final_params, open("final_params.pkl", 'wb'))
    print(final_params)

if MAKE_FINAL_EXPS:
    # final_params = {'input0': {'alpha': 0.1, 'exploration': 0.1, 'discount': 0.7}, 'input1': {'alpha': 0.1, 'exploration': 0.1, 'discount': 0.9}, 'input2': {'alpha': 0.5, 'exploration': 0.1, 'discount': 0.9}, 'input3': {'alpha': 0.1, 'exploration': 0.1, 'discount': 0.9}, 'input4': {
    #     'alpha': 0.1, 'exploration': 0.1, 'discount': 0.9}, 'input5': {'alpha': 0.1, 'exploration': 0.1, 'discount': 0.9}, 'input6': {'alpha': 0.3, 'exploration': 0.1, 'discount': 0.9}, 'input7': {'alpha': 0.9, 'exploration': 0.1, 'discount': 0.9}}

    final_params = pickle.load(open("final_params.pkl", 'rb'))

    args = []
    exp_name = "final"
    for map_path in maps:
        for i in range(REP):
            map_name = map_path.split("/")[-1].split(".")[0]
            exp_id = "exp_{}_{}_{}".format(map_name, exp_name, i)
            if not os.path.isfile(os.path.join("logs", exp_id, "qtable.pkl")):
                cmd = "python3 src/main.py --input {} -lr {} -y {} -e {} -id  {} -s".format(
                    map_path, final_params[map_name]["alpha"], final_params[map_name]["discount"], final_params[map_name]["exploration"], exp_id)
                args.append(cmd)

    parallel_args = chunker_list(args, parallel)
    files = [open("%i.sh" % i, 'w') for i in range(parallel)]
    final_file = open("run_all.sh", 'w')
    for i in range(parallel):
        for cmd in parallel_args[i]:
            files[i].write(cmd + " -t " + str(i) + "\n")

        files[i].close()
        final_file.write("sh %i.sh & " % i)
    final_file.close()

if MAKE_FINAL_GRAPHS:
    for map_path in maps:
        rewards = []
        for i in range(REP):
            map_name = map_path.split("/")[-1].split(".")[0]
            exp_id = "exp_{}_final_{}".format(map_name, i)

            info = pickle.load(
                open(os.path.join("logs", exp_id, "log.pkl"), "rb"))
            rewards.append(info["metrics"])
            plt.plot(moving_average(info["metrics"], 15),
                     alpha=0.2, color=CB_color_cycle[0])

        rewards = np.array(rewards)

        plt.plot(moving_average(np.mean(rewards, axis=0), 15),
                 color=CB_color_cycle[0])

        plt.title("Cumulative Rewards - {}".format(map_name))
        plt.tight_layout()
        plt.savefig("graphs/{}-final.png".format(map_name), dpi=200)
        plt.close()
