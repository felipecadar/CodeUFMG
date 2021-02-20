import pickle
import glob
import os
import numpy as np

import matplotlib as mpl
mpl.rcParams['figure.figsize'] = [12.0, 6.0]
from matplotlib import pyplot as plt

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def mkdirp(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory) 

colors = ["#0F54FF","#e41a1c","#984ea3","#377eb8","#ff7f00","#f781bf","#0FD0FF","#a65628","#dede00"]


exps_results = {}

for exp_folder in glob.glob("results/*/"):
    exp_name = exp_folder.split("/")[-2]

    single_exp = {}
    
    for exp_run in glob.glob(os.path.join(exp_folder, "*")):
        run_folder_name = os.path.split(exp_run)[1]
        if exp_name == "init_population":
            if "descend-prob" in run_folder_name or "ramped-hh" in run_folder_name :
                dataset_id, dataset_name, param1, param2, rep = run_folder_name.split("-")
                param = param1+"-"+param2
            else:
                dataset_id, dataset_name, param, rep = run_folder_name.split("-")
        else:
            dataset_id, dataset_name, param, rep = run_folder_name.split("-")
        rep = int(rep)

        log_filename = os.path.join(exp_run, "experiment_data.pkl")
        if os.path.isfile(log_filename):
        
            if not dataset_name in single_exp:
                single_exp[dataset_name] = {}

            if not param in single_exp[dataset_name]:
                single_exp[dataset_name][param] = {}


            data = pickle.load( open( log_filename, "rb" ) )
            single_exp[dataset_name][param][rep] = data
        else:
            print("Missing file", log_filename)

    exps_results[exp_name] = single_exp




##### Alpha exp:

linestyles = ["-", "--", "v"]
exp_name = "alpha"
full_exp = exps_results[exp_name]
for dataset_name in full_exp:
    mkdirp("plots/{}/".format(dataset_name))
    plots = {}    
    plots["all"] = 1
    plots["hist2d"] = 2
    plots["child_mutation"] = 3
    
    best_plots = []
    for idx, param in enumerate(sorted(full_exp[dataset_name])):

        total_crossover_hist = []
        total_mutation_branch_hist = []
        total_mutation_node_hist = []
        child_better_crossover_hist = []
        child_better_mutation_branch_hist = []
        child_better_mutation_node_hist = []


        for rep in full_exp[dataset_name][param]:
            data = full_exp[dataset_name][param][rep]

            total_crossover_hist.append(data["total_crossover_hist"])
            total_mutation_branch_hist.append(data["total_mutation_branch_hist"])
            total_mutation_node_hist.append(data["total_mutation_node_hist"])
            child_better_crossover_hist.append(data["child_better_crossover_hist"])
            child_better_mutation_branch_hist.append(data["child_better_mutation_branch_hist"])
            child_better_mutation_node_hist.append(data["child_better_mutation_node_hist"])
        

        ## Convert to numpy

        total_crossover_hist = np.array(total_crossover_hist)
        total_mutation_branch_hist = np.array(total_mutation_branch_hist)
        total_mutation_node_hist = np.array(total_mutation_node_hist)
        child_better_crossover_hist = np.array(child_better_crossover_hist)
        child_better_mutation_branch_hist = np.array(child_better_mutation_branch_hist)
        child_better_mutation_node_hist = np.array(child_better_mutation_node_hist)

        # ## Deal with zeros
        total_crossover_hist[total_crossover_hist == 0] = np.nan
        total_mutation_branch_hist[total_mutation_branch_hist == 0] = np.nan
        total_mutation_node_hist[total_mutation_node_hist == 0] = np.nan
        # child_better_crossover_hist[child_better_crossover_hist == 0] = np.nan
        # child_better_mutation_branch_hist[child_better_mutation_branch_hist == 0] = np.nan
        # child_better_mutation_node_hist[child_better_mutation_node_hist == 0] = np.nan
        
        child_better_mutation_hist = (child_better_mutation_node_hist + child_better_mutation_branch_hist) / (total_mutation_node_hist + total_mutation_branch_hist)
        child_better_mutation_node_hist /= total_mutation_node_hist 
        child_better_mutation_branch_hist /= total_mutation_branch_hist 
        child_better_crossover_hist /= total_crossover_hist 

        plt.figure(plots["all"])
        plt.plot(moving_average(np.nanmean(child_better_mutation_hist, axis=0)[1:], 15), label=param + " Mutation", color=colors[idx % 9])
        plt.plot(moving_average(np.nanmean(child_better_crossover_hist, axis=0)[1:], 15), label=param + " Crossover", color=colors[idx % 9], linestyle="--")


    plt.figure(plots["all"])
    plt.legend(title=exp_name, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.title("{} - Porcentagem de Filhos Melhores".format(dataset_name))
    plt.tight_layout()
    # plt.savefig('plots/{}/{}-best_child.png'.format(dataset_name, exp_name), dpi=300)
    plt.savefig('plots/{}/{}-best_child.pdf'.format(dataset_name, exp_name), dpi=300)
    plt.clf()

for exp_name in exps_results:
    full_exp = exps_results[exp_name]
    for dataset_name in full_exp:
        mkdirp("plots/{}/".format(dataset_name))
        plots = {}    
        plots["best_fit"] = 1
        plots["mean_fit"] = 2
        plots["worse_fit"] = 3
        plots["mean_mutation_node_fit"] = 4
        plots["mean_mutation_branch_fit"] = 5
        plots["mean_crossover_fit"] = 6
        plots["unique_ind_hist"] = 7
        
        best_plots = []
        for idx, param in enumerate(sorted(full_exp[dataset_name])):

            mean_fit_mutation_branch_hist = []
            mean_fit_mutation_node_hist = []
            mean_fit_crossover_hist = []
            mean_fit_mutation_branch_child_hist = []
            mean_fit_mutation_node_child_hist = []
            mean_fit_crossover_child_hist = []

            best_fit_hist = []
            worse_fit_hist = []
            mean_fit_hist = []
            unique_ind_hist = []


            for rep in full_exp[dataset_name][param]:
                data = full_exp[dataset_name][param][rep]

                best_fit_hist.append(data["best_fit_hist"])
                worse_fit_hist.append(data["worse_fit_hist"])
                mean_fit_hist.append(data["mean_fit_hist"])
                unique_ind_hist.append(data["unique_ind_hist"])

                mean_fit_mutation_branch_hist.append(data["mean_fit_mutation_branch_hist"])
                mean_fit_mutation_node_hist.append(data["mean_fit_mutation_node_hist"])
                mean_fit_crossover_hist.append(data["mean_fit_crossover_hist"])
                mean_fit_mutation_branch_child_hist.append(data["mean_fit_mutation_branch_child_hist"])
                mean_fit_mutation_node_child_hist.append(data["mean_fit_mutation_node_child_hist"])
                mean_fit_crossover_child_hist.append(data["mean_fit_crossover_child_hist"])
            

            ## Convert to numpy
            best_fit_hist = np.array(best_fit_hist)
            worse_fit_hist = np.array(worse_fit_hist)
            mean_fit_hist = np.array(mean_fit_hist)
            unique_ind_hist = np.array(unique_ind_hist)

            mean_fit_mutation_branch_hist = np.array(mean_fit_mutation_branch_hist)
            mean_fit_mutation_node_hist = np.array(mean_fit_mutation_node_hist)
            mean_fit_crossover_hist = np.array(mean_fit_crossover_hist)
            mean_fit_mutation_branch_child_hist = np.array(mean_fit_mutation_branch_child_hist)
            mean_fit_mutation_node_child_hist = np.array(mean_fit_mutation_node_child_hist)
            mean_fit_crossover_child_hist = np.array(mean_fit_crossover_child_hist)

            ## Deal with early stops
            best_fit_hist[best_fit_hist == 0] = np.nan
            worse_fit_hist[worse_fit_hist == 0] = np.nan
            mean_fit_hist[mean_fit_hist == 0] = np.nan
            unique_ind_hist[unique_ind_hist == 0] = np.nan

            # mean_fit_mutation_branch_hist[mean_fit_mutation_branch_hist == 0] = np.nan
            # mean_fit_mutation_node_hist[mean_fit_mutation_node_hist == 0] = np.nan
            # mean_fit_crossover_hist[mean_fit_crossover_hist == 0] = np.nan
            # mean_fit_mutation_branch_child_hist[mean_fit_mutation_branch_child_hist == 0] = np.nan
            # mean_fit_mutation_node_child_hist[mean_fit_mutation_node_child_hist == 0] = np.nan
            # mean_fit_crossover_child_hist[mean_fit_crossover_child_hist == 0] = np.nan
            
            ## Filter Big values
            best_fit_hist[best_fit_hist > 100 ] = 100
            worse_fit_hist[worse_fit_hist > 100 ] = 100
            mean_fit_hist[mean_fit_hist > 100 ] = 100
            # unique_ind_hist[unique_ind_hist > 100 ] = 100

            mean_fit_mutation_branch_hist[mean_fit_mutation_branch_hist > 100 ] = 100
            mean_fit_mutation_node_hist[mean_fit_mutation_node_hist > 100 ] = 100
            mean_fit_crossover_hist[mean_fit_crossover_hist > 100 ] = 100
            mean_fit_mutation_branch_child_hist[mean_fit_mutation_branch_child_hist > 100 ] = 100
            mean_fit_mutation_node_child_hist[mean_fit_mutation_node_child_hist > 100 ] = 100
            mean_fit_crossover_child_hist[mean_fit_crossover_child_hist > 100 ] = 100

            plt.figure(plots["best_fit"])
            plt.plot(np.nanmean(best_fit_hist, axis=0), label=param, color=colors[idx % 9])
            
            plt.figure(plots["mean_fit"])
            plt.plot(np.nanmean(mean_fit_hist, axis=0), label=param, color=colors[idx % 9])

            plt.figure(plots["worse_fit"])
            plt.plot(np.nanmean(worse_fit_hist, axis=0), label=param, color=colors[idx % 9])

            # plt.figure(plots["mean_mutation_branch_fit"])
            # plt.plot(np.nanmean(mean_fit_mutation_branch_hist, axis=0), label=param+" parent", color=colors[idx % 9])
            # plt.plot(np.nanmean(mean_fit_mutation_branch_child_hist, axis=0), label=param+" child", linestyle="dashed", color=colors[idx % 9])

            # plt.figure(plots["mean_mutation_node_fit"])
            # plt.plot(np.nanmean(mean_fit_mutation_node_hist, axis=0), label=param+" parent", color=colors[idx % 9])
            # plt.plot(np.nanmean(mean_fit_mutation_node_child_hist, axis=0), label=param+" child", linestyle="dashed", color=colors[idx % 9])

            # plt.figure(plots["mean_crossover_fit"])
            # plt.plot(np.nanmean(mean_fit_crossover_hist, axis=0), label=param+" parent", color=colors[idx % 9])
            # plt.plot(np.nanmean(mean_fit_crossover_child_hist, axis=0), label=param+" child", linestyle="dashed", color=colors[idx % 9])

            plt.figure(plots["unique_ind_hist"])
            plt.plot(np.nanmean(unique_ind_hist, axis=0), label=param, color=colors[idx % 9])


        plt.figure(plots["best_fit"])
        plt.legend(title=exp_name, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.ylabel("Fitness")
        plt.xlabel("Geração")
        plt.title("{} - Melhor fitness por geração".format(dataset_name))
        plt.tight_layout()
        # plt.savefig('plots/{}/{}-best_fit.png'.format(dataset_name, exp_name), dpi=300)
        plt.savefig('plots/{}/{}-best_fit.pdf'.format(dataset_name, exp_name), dpi=300)
        plt.clf()

        plt.figure(plots["mean_fit"])
        plt.legend(title=exp_name, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.title("{} - Fitness média por geração".format(dataset_name))
        plt.tight_layout()
        # plt.savefig('plots/{}/{}-means_fit.png'.format(dataset_name, exp_name), dpi=300)
        plt.savefig('plots/{}/{}-means_fit.pdf'.format(dataset_name, exp_name), dpi=300)
        plt.clf()

        plt.figure(plots["worse_fit"])
        plt.legend(title=exp_name, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.title("{} - Pior fitness por geração".format(dataset_name))
        plt.tight_layout()
        # plt.savefig('plots/{}/{}-worse_fit.png'.format(dataset_name, exp_name), dpi=300)
        plt.savefig('plots/{}/{}-worse_fit.pdf'.format(dataset_name, exp_name), dpi=300)
        plt.clf()

        plt.figure(plots["unique_ind_hist"])
        plt.legend(title=exp_name, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.title("{} - Individuos únicos por geração".format(dataset_name))
        plt.ylabel("Quantidade de indivíduos únicos")
        plt.xlabel("Geração")
        plt.tight_layout()
        # plt.savefig('plots/{}/{}-unique_ind_hist.png'.format(dataset_name, exp_name), dpi=300)
        plt.savefig('plots/{}/{}-unique_ind_hist.pdf'.format(dataset_name, exp_name), dpi=300)
        plt.clf()


        # plt.show()

