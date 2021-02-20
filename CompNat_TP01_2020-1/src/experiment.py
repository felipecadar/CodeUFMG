import glob
import os
import sys

def mkdirp(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory) 

REP = 30

default_args = {
    "--stop": 0,
    "--gen": 1000,
    "--size": 50,
    # "--seed": 1000,
    "--K": 20,
    "--alpha":0.9,
    "--fitness": "MSE",
    "--population": "ramped-hh",
    "--depth": 7,
    "--elit":"",
}

files = sorted(glob.glob("datasets/*.txt"))

## Population Size Experiments

variable = [10, 50, 100, 300, 500]
exp_size = len(variable) * len(files) * REP
exp_counter = 0
mkdirp("exp")
with open("exp/pop_exp.sh", "w") as exp_file:
    for dataset in files:
        for i in range(REP):
            for var in variable:
                exp_dict = default_args.copy()
                exp_dict["--output"] = "results/pop_size"
                exp_dict["--input"] = dataset
                exp_dict["--size"] = var
                exp_dict["--id"] = "{}-{}-{}".format(os.path.basename(dataset).split(".")[0], var, i)

                final_path = os.path.join("results/pop_size",  exp_dict["--id"])
                # mkdirp(final_path)

                cmd = "python3 src/main.py "
                for key, value in exp_dict.items():
                    cmd += key + " "
                    cmd += str(value) + " "
                cmd += " > {}".format(os.path.join(final_path, "run.log"))

                exp_file.write("echo 'Running PopSize exp {}/{}' ".format(exp_counter, exp_size) + "\n")
                exp_file.write("mkdir -p {}\n".format(final_path))
                exp_file.write(cmd + "\n")

                exp_counter += 1

## Elitism Experiments

variable = ["Elit", "NotElit"]
exp_size = len(variable) * len(files) * REP
exp_counter = 0
with open("exp/elit_exp.sh", "w") as exp_file:
    for dataset in files:
        for i in range(REP):
            for var in variable:
                exp_dict = default_args.copy()

                exp_dict["--output"] = "results/elit"
                exp_dict["--input"] = dataset
                exp_dict["--id"] = "{}-{}-{}".format(os.path.basename(dataset).split(".")[0], var, i)

                if var == "NotElit":
                    del exp_dict["--elit"]

                final_path = os.path.join("results/elit",  exp_dict["--id"])
                # mkdirp(final_path)

                cmd = "python3 src/main.py "
                for key, value in exp_dict.items():
                    cmd += key + " "
                    cmd += str(value) + " "
                cmd += " > {}".format(os.path.join(final_path, "run.log"))

                exp_file.write("echo 'Running Elit exp {}/{}' ".format(exp_counter, exp_size) + "\n")
                exp_file.write("mkdir -p {}\n".format(final_path))
                exp_file.write(cmd + "\n")

                exp_counter += 1

## Alpha Experiments

variable = [0.9, 0.6, 0.3]
exp_size = len(variable) * len(files) * REP
exp_counter = 0
with open("exp/alpha_exp.sh", "w") as exp_file:
    for dataset in files:
        for i in range(REP):
            for var in variable:
                exp_dict = default_args.copy()

                exp_dict["--output"] = "results/alpha"
                exp_dict["--input"] = dataset
                exp_dict["--id"] = "{}-{}-{}".format(os.path.basename(dataset).split(".")[0], var, i)
                exp_dict["--alpha"] = var

                final_path = os.path.join("results/alpha",  exp_dict["--id"])
                # mkdirp(final_path)

                cmd = "python3 src/main.py "
                for key, value in exp_dict.items():
                    cmd += key + " "
                    cmd += str(value) + " "
                cmd += " > {}".format(os.path.join(final_path, "run.log"))

                exp_file.write("echo 'Running Alpha exp {}/{}' ".format(exp_counter, exp_size) + "\n")
                exp_file.write("mkdir -p {}\n".format(final_path))
                exp_file.write(cmd + "\n")

                exp_counter += 1

## K Experiments

variable = [2, 5, 10, 20]
exp_size = len(variable) * len(files) * REP
exp_counter = 0
with open("exp/K_exp.sh", "w") as exp_file:
    for dataset in files:
        for i in range(REP):
            for var in variable:
                exp_dict = default_args.copy()

                exp_dict["--output"] = "results/K"
                exp_dict["--input"] = dataset
                exp_dict["--id"] = "{}-{}-{}".format(os.path.basename(dataset).split(".")[0], var, i)
                exp_dict["--K"] = var

                final_path = os.path.join("results/K",  exp_dict["--id"])
                # mkdirp(final_path)

                cmd = "python3 src/main.py "
                for key, value in exp_dict.items():
                    cmd += key + " "
                    cmd += str(value) + " "
                cmd += " > {}".format(os.path.join(final_path, "run.log"))

                exp_file.write("echo 'Running K exp {}/{}' ".format(exp_counter, exp_size) + "\n")
                exp_file.write("mkdir -p {}\n".format(final_path))
                exp_file.write(cmd + "\n")

                exp_counter += 1



## Fitness Experiments

variable = ["ABS","MSE","RMSE"]
exp_size = len(variable) * len(files) * REP
exp_counter = 0
with open("exp/fitness_exp.sh", "w") as exp_file:
    for dataset in files:
        for i in range(REP):
            for var in variable:
                exp_dict = default_args.copy()

                exp_dict["--output"] = "results/fitness"
                exp_dict["--input"] = dataset
                exp_dict["--id"] = "{}-{}-{}".format(os.path.basename(dataset).split(".")[0], var, i)
                exp_dict["--fitness"] = var

                final_path = os.path.join("results/fitness",  exp_dict["--id"])
                # mkdirp(final_path)

                cmd = "python3 src/main.py "
                for key, value in exp_dict.items():
                    cmd += key + " "
                    cmd += str(value) + " "
                cmd += " > {}".format(os.path.join(final_path, "run.log"))

                exp_file.write("echo 'Running Fitness exp {}/{}' ".format(exp_counter, exp_size) + "\n")
                exp_file.write("mkdir -p {}\n".format(final_path))
                exp_file.write(cmd + "\n")

                exp_counter += 1

## InitPopulation Experiments

variable = ["ramped-hh","full","grow", "descend-prob"]
exp_size = len(variable) * len(files) * REP
exp_counter = 0
with open("exp/init_population_exp.sh", "w") as exp_file:
    for dataset in files:
        for i in range(REP):
            for var in variable:
                exp_dict = default_args.copy()

                exp_dict["--output"] = "results/init_population"
                exp_dict["--input"] = dataset
                exp_dict["--id"] = "{}-{}-{}".format(os.path.basename(dataset).split(".")[0], var, i)
                exp_dict["--population"] = var

                final_path = os.path.join("results/init_population",  exp_dict["--id"])
                # mkdirp(final_path)

                cmd = "python3 src/main.py "
                for key, value in exp_dict.items():
                    cmd += key + " "
                    cmd += str(value) + " "
                cmd += " > {}".format(os.path.join(final_path, "run.log"))

                exp_file.write("echo 'Running InitPopulation exp {}/{}' ".format(exp_counter, exp_size) + "\n")
                exp_file.write("mkdir -p {}\n".format(final_path))
                exp_file.write(cmd + "\n")

                exp_counter += 1