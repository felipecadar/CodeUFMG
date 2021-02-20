import numpy as np
import  matplotlib.pyplot as plt

popsize = 50
tournament_sizes = [2,3,4,5,6,7,8,9,10]
tournament_sizes_legend = ['k = 2','k = 3','k = 4','k = 5','k = 6','k = 7','k = 8','k = 9','k = 10',]
generation = 500
mutation = 0.05
cores = 30
dataset = 'datasets/synth1/synth1-train.csv' 
max_level = 6 
threshold = 0.001
el = " " 
exp_id = 0
log = "log/k/"

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


for tournament_size in tournament_sizes:
    e = np.zeros([generation + 1, 3])
    for i in range(30): #repeat 30 times
        exp_id = i
        name = "log/k/id_{}__p_{}__k_{}__g_{}__m_{}__c_{}__d_{}__md_{}__t_{}.txt".format(exp_id, popsize, tournament_size,generation, mutation, cores, dataset.split('/')[-1].split('.')[0] ,max_level, threshold)
        a = readFile(name, generation, popsize)
    
        a1 = np.amax(a, axis=1)
        a2 = np.amin(a, axis=1)
        a3 = np.mean(a, axis=1)

        # print e[:, 0].shape
        # print (min(a3))

        e[:,0] += a1    
        e[:,1] += a2    
        e[:,2] += a3    
    
    e = e/30.

    fits.append(e)

for i in range(3):
    plt.subplot(3,1,i+1)
    for j in range(9):
        # print fits[j][0:10,i]
        plt.plot(fits[j][:,i])
       
    plt.legend(tournament_sizes_legend, loc='upper left')
    
    
plt.show()