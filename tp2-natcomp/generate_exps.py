import sys, os, pickle
from random import shuffle


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

command = '''
for (( i = 0; i < ${#arr[@]} ; i++ )); do
    printf "\\n**** Running: (${i}/${#arr[@]}) ${arr[$i]} *****\\n\\n"
    eval "${arr[$i]}"
done
'''

divisions = 1
sep = list(range(divisions))
exp_sh = []
for i in sep:
    exp_sh.append(open("run_{}.sh".format(i), "w"))

def_executions = 10
def_popsize = 200
def_cycles = 100
def_p = 0.9
def_initial_trail = 10
def_q = 4
def_cores = 30
def_alpha = 3
def_beta = 1

# datasets = ["datasets/graph1.txt", "datasets/graph2.txt"]
datasets = ["datasets/graph2.txt"]
popsize = [10,20,30,40,50] 
cycles = [50,100,200,300]
exp_id = 0
p = [0.3,0.5,0.7,0.9]
q = [1,10,100,1000]
alpha = [0,0.5,1,2,5]
beta = [0,0.5,1,2,5]


exp_types = ["a", "b", "q", "p", "cycle", "pop"]
params = {"pop":popsize, "cycle":cycles, "p":p, "q":q, "a":alpha, "b":beta}
exp_paths = {"a":"sensitivity_analysis/a/", "b":"sensitivity_analysis/b/", "q":"sensitivity_analysis/q/", "p":"sensitivity_analysis/p/", "cycle":"sensitivity_analysis/cycle/", "pop":"sensitivity_analysis/pop/"}

for x in exp_paths:
    for d in datasets:
        ensure_dir("{}{}/".format(exp_paths[x], d.split(".")[0]))

all_exps = []
for typ in exp_types:
    exp_id = 0
    for param in params[typ]:
        for dataset in datasets:
            pk_path = "{}{}/exp_{}.pk".format(exp_paths[typ], dataset.split(".")[0], exp_id)
            log_dir = "log/{}{}/".format(exp_paths[typ], dataset.split(".")[0])
            all_exps.append(pk_path)
            if typ == "a":
                args = [ dataset, def_popsize, def_cycles, log_dir, exp_id, def_p, def_initial_trail, def_q, def_cores, param, def_beta]
            if typ == "b":
                args = [ dataset, def_popsize, def_cycles, log_dir, exp_id, def_p, def_initial_trail, def_q, def_cores, def_alpha, param]
            if typ == "q":
                args = [ dataset, def_popsize, def_cycles, log_dir, exp_id, def_p, def_initial_trail, param, def_cores, def_alpha, def_beta]
            if typ == "p":
                args = [ dataset, def_popsize, def_cycles, log_dir, exp_id, param, def_initial_trail, def_q, def_cores, def_alpha, def_beta]
            if typ == "cycle":
                args = [ dataset, def_popsize, param, log_dir, exp_id, def_p, def_initial_trail, def_q, def_cores, def_alpha, def_beta]
            if typ == "pop":
                args = [ dataset, param, def_cycles, log_dir, exp_id, def_p, def_initial_trail, def_q, def_cores, def_alpha, def_beta]
            
            pickle.dump(args, open(pk_path, 'wb'))

        exp_id += 1

for s in sep:
    exp_sh[s].write("declare -a arr=(")

shuffle(all_exps)
for i in range(len(all_exps)):
    for s in sep:
        if i % divisions == s:
            for ex in range(def_executions):
                exp_sh[s].write("\"python3 src/main.py -pk {}\"\n".format(all_exps[i]))

for s in sep:
    exp_sh[s].write(")")
    exp_sh[s].write(command)
