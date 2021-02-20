import glob
import os
import sys

def mkdirp(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory) 

REP = 30



exp_size = 5 * REP
exp_counter = 0

mkdirp("exp/")
with open("exp/final.sh", "w") as exp_file:

    
    dataset = "datasets/01-SR_div.txt"
    default_args = {
        "--stop": 0.01,
        "--gen": 100,
        "--size": 500,
        "--K": 2,
        "--alpha":0.3,
        "--fitness": "MSE",
        "--population": "descend-prob",
        "--depth": 7,
        "--elit":"",
        "--output": "results/final/",
        "--input": dataset
    }

    for i in range(REP):
        exp_dict = default_args.copy()
        exp_dict["--id"] = "final-{}-{}".format(os.path.basename(dataset).split(".")[0], i)

        final_path = os.path.join("results/final/",  exp_dict["--id"])
        # mkdirp(final_path)

        cmd = "python3 src/main.py "
        for key, value in exp_dict.items():
            cmd += key + " "
            cmd += str(value) + " "
        cmd += " > {}".format(os.path.join(final_path, "run.log"))

        exp_file.write("echo 'Running Final exp {}/{}' ".format(exp_counter, exp_size) + "\n")
        exp_file.write("mkdir -p {}\n".format(final_path))
        exp_file.write(cmd + "\n")

        exp_counter += 1
        
        
    dataset = "datasets/02-SR_div_noise.txt"
    default_args = {
        "--stop": 0.01,
        "--gen": 100,
        "--size": 500,
        "--K": 2,
        "--alpha":0.6,
        "--fitness": "MSE",
        "--population": "grow",
        "--depth": 7,
        "--elit":"",
        "--output": "results/final/",
        "--input": dataset
    }

    for i in range(REP):
        exp_dict = default_args.copy()
        exp_dict["--id"] = "final-{}-{}".format(os.path.basename(dataset).split(".")[0], i)

        final_path = os.path.join("results/final/",  exp_dict["--id"])
        # mkdirp(final_path)

        cmd = "python3 src/main.py "
        for key, value in exp_dict.items():
            cmd += key + " "
            cmd += str(value) + " "
        cmd += " > {}".format(os.path.join(final_path, "run.log"))

        exp_file.write("echo 'Running Final exp {}/{}' ".format(exp_counter, exp_size) + "\n")
        exp_file.write("mkdir -p {}\n".format(final_path))
        exp_file.write(cmd + "\n")

        exp_counter += 1
        
    dataset = "datasets/03-SR_ellipse_noise.txt"
    default_args = {
        "--stop": 0.01,
        "--gen": 100,
        "--size": 10,
        "--K": 5,
        "--alpha":0.6,
        "--fitness": "MSE",
        "--population": "grow",
        "--depth": 7,
        "--elit":"",
        "--output": "results/final/",
        "--input": dataset
    }

    for i in range(REP):
        exp_dict = default_args.copy()
        exp_dict["--id"] = "final-{}-{}".format(os.path.basename(dataset).split(".")[0], i)

        final_path = os.path.join("results/final/",  exp_dict["--id"])
        # mkdirp(final_path)

        cmd = "python3 src/main.py "
        for key, value in exp_dict.items():
            cmd += key + " "
            cmd += str(value) + " "
        cmd += " > {}".format(os.path.join(final_path, "run.log"))

        exp_file.write("echo 'Running Final exp {}/{}' ".format(exp_counter, exp_size) + "\n")
        exp_file.write("mkdir -p {}\n".format(final_path))
        exp_file.write(cmd + "\n")

        exp_counter += 1 
 
    dataset = "datasets/04-SR_circle.txt"
    default_args = {
        "--stop": 0.01,
        "--gen": 100,
        "--size": 50,
        "--K": 2,
        "--alpha":0.6,
        "--fitness": "MSE",
        "--population": "grow",
        "--depth": 7,
        "--elit":"",
        "--output": "results/final/",
        "--input": dataset
    }

    for i in range(REP):
        exp_dict = default_args.copy()
        exp_dict["--id"] = "final-{}-{}".format(os.path.basename(dataset).split(".")[0], i)

        final_path = os.path.join("results/final/",  exp_dict["--id"])
        # mkdirp(final_path)

        cmd = "python3 src/main.py "
        for key, value in exp_dict.items():
            cmd += key + " "
            cmd += str(value) + " "
        cmd += " > {}".format(os.path.join(final_path, "run.log"))

        exp_file.write("echo 'Running Final exp {}/{}' ".format(exp_counter, exp_size) + "\n")
        exp_file.write("mkdir -p {}\n".format(final_path))
        exp_file.write(cmd + "\n")

        exp_counter += 1


    dataset = "datasets/00-concrete.txt"
    default_args = {
        "--stop": 0.01,
        "--gen": 800,
        "--size": 300,
        "--K": 5,
        "--alpha":0.3,
        "--fitness": "MSE",
        "--population": "grow",
        "--depth": 7,
        "--elit":"",
        "--output": "results/final/",
        "--input": dataset
    }

    for i in range(REP):
        exp_dict = default_args.copy()
        exp_dict["--id"] = "final-{}-{}".format(os.path.basename(dataset).split(".")[0], i)

        final_path = os.path.join("results/final/",  exp_dict["--id"])
        # mkdirp(final_path)

        cmd = "python3 src/main.py "
        for key, value in exp_dict.items():
            cmd += key + " "
            cmd += str(value) + " "
        cmd += " > {}".format(os.path.join(final_path, "run.log"))

        exp_file.write("echo 'Running Final exp {}/{}' ".format(exp_counter, exp_size) + "\n")
        exp_file.write("mkdir -p {}\n".format(final_path))
        exp_file.write(cmd + "\n")

        exp_counter += 1