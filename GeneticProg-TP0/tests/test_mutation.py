import os

popsize = 50
tournament_size = 7
generation = 500
mutations = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
cores = 30
datasets = ['datasets/concrete/concrete-train.csv', 'datasets/synth1/synth1-train.csv', 'datasets/synth2/synth2-train.csv'] 
max_level = 6 
threshold = 0.001
el = " " 
exp_id = 0
log = "log/m/"

for dataset in datasets:
    for i in range(30): #repeat 30 times
        exp_id = i
        for mutation in mutations:
            command = "python3 main.py -id {} -p {} -k {} -g {} -m {} -c {} -d {} -md {} -t {} -lg {} {}".format(exp_id, popsize, tournament_size, generation, mutation, cores, dataset ,max_level, threshold, log,  el)
            print(command)
        