import os

popsizes = [50, 100, 500]
tournament_size = 7
generations = [50, 100, 500]
mutation = 0.05
cores = 30
datasets = ['datasets/concrete/concrete-train.csv', 'datasets/synth1/synth1-train.csv', 'datasets/synth2/synth2-train.csv'] 
max_level = 6 
threshold = 0.001
elitismo = " " 
exp_id = 0
log = "log/pop/"

for dataset in datasets:
    for i in range(30): #repeat 30 times
        exp_id = i
        for popsize in popsizes:
            for generation in generations:
                command = "python3 main.py -id {} -p {} -k {} -g {} -m {} -c {} -d {} -md {} -t {} -lg {} {}".format(exp_id, popsize, tournament_size, generation, mutation, cores, dataset ,max_level, threshold, log,  elitismo)
                print(command)