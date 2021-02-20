import os
import sys
import ast
import glob
import pickle
import numpy as np
import matplotlib.pyplot as plt

dir_path = "log/sensitivity_analysis/q/datasets/graph1/"

exps = ['0', '1', '2', '3']
rep  = 10

fig, axs = plt.subplots(3, 1, constrained_layout=True)

legend = []

parms_file = dir_path.replace("log/", "")+"/exp_0.pk"
dataset, popsize, cycles, log_dir, exp_id, p, initial_trail, q, cores, alpha, beta = pickle.load( open( parms_file, "rb" ) )
general_max = np.zeros([cycles, rep])
general_min = np.zeros([cycles, rep])
general_mean = np.zeros([cycles, rep])
for k in range(len(exps)):
    exp = exps[k]
    parms_file = dir_path.replace("log/", "")+"/exp_{}.pk".format(exp)
    dataset, popsize, cycles, log_dir, exp_id, p, initial_trail, q, cores, alpha, beta = pickle.load( open( parms_file, "rb" ) )
    legend.append(str(q))
    for i in range(rep):
        filename = dir_path+"/expid_{}_rep_{}.txt".format(exp, i)
        lines = open(filename, 'r').readlines()[1:]
        for j in range(len(lines)):
            x = np.array(ast.literal_eval(lines[j]))
            x = np.delete(x, np.where(x == 0))
            general_max[j][i] = np.max(x)
            general_min[j][i] = np.min(x)
            general_mean[j][i] = np.mean(x)

    final_max = np.amax(general_max, 1)
    final_min = np.amin(general_min, 1)
    final_mean = np.mean(general_mean, 1)

    axs[0].plot(final_max)
    axs[1].plot(final_min)
    axs[2].plot(final_mean)


axs[0].legend(legend, loc='upper left')
axs[0].set_xlabel("Cycle")
axs[0].set_ylabel("Distance")
axs[0].set_title("Max Distances")

axs[1].legend(legend, loc='upper left')
axs[1].set_xlabel("Cycle")
axs[1].set_ylabel("Distance")
axs[1].set_title("Min Distances")

axs[2].legend(legend, loc='upper left')
axs[2].set_xlabel("Cycle")
axs[2].set_ylabel("Distance")
axs[2].set_title("Mean Distances")

fig.suptitle("Trail Regulator Graph 1")

plt.draw()
plt.show()
fig.savefig(dir_path.replace("log/", "")+"/graph.svg", bbox_inches='tight')
# fig.savefig(dir_path.replace("log/", "")+"/graph.svg")