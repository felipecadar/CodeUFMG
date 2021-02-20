import os

popsize = 50
tournament_sizes = [2,3,4,5,6,7,8,9,10]
generation = 500
mutation = 0.05
cores = 30
datasets = ['datasets/concrete/concrete-train.csv', 'datasets/synth1/synth1-train.csv', 'datasets/synth2/synth2-train.csv'] 
max_level = 6 
threshold = 0.001
el = " " 
exp_id = 0
log = "log/k/"

for dataset in datasets:
    for i in range(30): #repeat 30 times
        exp_id = i
        for tournament_size in tournament_sizes:
            command = "python3 main.py -id {} -p {} -k {} -g {} -m {} -c {} -d {} -md {} -t {} -lg {} {}".format(exp_id, popsize, tournament_size, generation, mutation, cores, dataset ,max_level, threshold, log,  el)
            print(command)
        