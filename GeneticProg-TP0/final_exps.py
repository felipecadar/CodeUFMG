import os

popsize = 500
tournament_size = 6
generation = 500
mutation = 0.4
cores = 20
datasets = ['datasets/concrete/concrete-train.csv', 'datasets/synth1/synth1-train.csv', 'datasets/synth2/synth2-train.csv'] 
max_level = 6 
threshold = 0.001
el = " " 
exp_id = 0
log = "log/final/"

for dataset in datasets:
    for i in range(30): #repeat 30 times
        exp_id = i
        command = "python3 main.py -id {} -p {} -k {} -g {} -m {} -c {} -d {} -md {} -t {} -lg {} {}".format(exp_id, popsize, tournament_size, generation, mutation, cores, dataset ,max_level, threshold, log,  el)
        print(command)
        
