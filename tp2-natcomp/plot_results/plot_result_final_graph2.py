import os
import sys
import ast
import glob
import pickle
import numpy as np
import matplotlib.pyplot as plt

dir_path = "final_graph2"

fig, axs = plt.subplots(3, 1, constrained_layout=True)

legend = []
cycles = 200
rep = 10

exp = '2'

for i in range(rep):
    filename = dir_path+"/expid_{}_rep_{}.txt".format(exp, i)
    lines = open(filename, 'r').readlines()[1:]
    legend.append(str(i))
    final_max = []
    final_min = []
    final_mean = []
    print(len(lines))
    for j in range(len(lines)):
        x = np.array(ast.literal_eval(lines[j]))
        # x = np.delete(x, np.where(x == 0))
        final_max.append(np.max(x))
        final_min.append(np.min(x))
        final_mean.append(np.mean(x))

    axs[0].plot(list(range(len(final_max))), final_max)
    axs[1].plot(list(range(len(final_min))) ,final_min)
    axs[2].plot(list(range(len(final_mean))) ,final_mean)


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

fig.suptitle("Final Graph 2")

plt.draw()
plt.show()
fig.savefig(dir_path.replace("log/", "")+"/graph.svg", bbox_inches='tight')
# fig.savefig(dir_path.replace("log/", "")+"/graph.svg")