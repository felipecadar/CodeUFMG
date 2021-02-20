import numpy as np
import  matplotlib.pyplot as plt

popsize = 50
tournament_size = 7
generation = 250
mutation = 0.05
cores = 3
datasets = ['datasets/synth1/synth1-train.csv'] 
max_level = 6 
threshold = 0.001
elitismo = ["True", "False"] 
exp_id = 0
log = "log/el/"

fits = []

def readFile(name, gen, popsize):
    f = open(name, 'r')
    i = 0
    all_lines = f.readlines()
    fits = np.zeros([gen+1, popsize])
    for line in all_lines:
        if not line.startswith("-->"):
            fits[i] = np.fromstring(line, dtype=float, sep=',')
            i += 1

    return fits

for dataset in datasets:
    for i in range(30): #repeat 30 times
        exp_id = i
        e = []
        for el in elitismo:
            name = "log/el/id_{}__p_{}__k_{}__g_{}__m_{}__c_{}__d_{}__md_{}__t_{}__el_{}.txt".format(exp_id, popsize, tournament_size,generation, mutation, cores, dataset.split('/')[-1].split('.')[0] ,max_level, threshold, el)
            e.append(readFile(name, generation, popsize))

        fits.append(e)


with_max_fits = np.zeros([generation + 1])
with_min_fits = np.zeros([generation + 1])
with_mean_fits = np.zeros([generation + 1])

without_max_fits = np.zeros([generation + 1])
without_min_fits = np.zeros([generation + 1])
without_mean_fits = np.zeros([generation + 1])

for fit in fits:

    with_max_fits += np.amax(fit[0], axis=1)
    without_max_fits += np.amax(fit[1], axis=1)

    with_min_fits += np.amin(fit[0], axis=1)
    without_min_fits += np.amin(fit[1], axis=1)

    with_mean_fits += np.mean(fit[0], axis=1)
    without_mean_fits += np.mean(fit[1], axis=1)


with_max_fits = with_max_fits / 30
without_max_fits = without_max_fits / 30

with_min_fits = with_min_fits / 30
without_min_fits = without_min_fits / 30

with_mean_fits = with_mean_fits / 30
without_mean_fits = without_mean_fits / 30

plt.subplot(3,1,1)
plt.plot(with_max_fits)
plt.plot(without_max_fits)
plt.legend(['with', 'without'], loc='upper left')

plt.subplot(3,1,3)
plt.plot(with_mean_fits)
plt.plot(without_mean_fits)
plt.legend(['with', 'without'], loc='upper left')

plt.subplot(3,1,2)
plt.plot(with_min_fits)
plt.plot(without_min_fits)
plt.legend(['with', 'without'], loc='upper left')
    
plt.show()