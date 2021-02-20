import pickle
import glob
import os
import numpy as np
from tools import *

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

datasets = ["00-concrete", "01-SR_div", "02-SR_div_noise", "03-SR_ellipse_noise", "04-SR_circle"]
for dataset in datasets:
    single_exp = {}
    for exp_folder in glob.glob("final/*{}*/".format(dataset)):
        rep = int(exp_folder.split("-")[-1].replace("/",""))

        log_filename = os.path.join(exp_folder, "experiment_data.pkl")
        if os.path.isfile(log_filename):

            data = pickle.load( open( log_filename, "rb" ) )
            single_exp[rep] = data
        else:
            print("Missing file", log_filename)

    exps_results[dataset] = single_exp




##### Alpha exp:

linestyles = ["-", "--", "v"]
for dataset_name in exps_results:
    mkdirp("plots/final/{}/".format(dataset_name))
    plots = {}    
    plots["all"] = 1
    plots["hist2d"] = 2
    plots["child_mutation"] = 3
    
    best_plots = []

    total_crossover_hist = []
    total_mutation_branch_hist = []
    total_mutation_node_hist = []
    child_better_crossover_hist = []
    child_better_mutation_branch_hist = []
    child_better_mutation_node_hist = []

    for rep in exps_results[dataset_name]:
        data = exps_results[dataset_name][rep]

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
    plt.plot(moving_average(np.nanmean(child_better_mutation_hist, axis=0)[1:], 15), label=" Mutation")
    plt.plot(moving_average(np.nanmean(child_better_crossover_hist, axis=0)[1:], 15), label=" Crossover", linestyle="--")


    plt.figure(plots["all"])
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.title("{} - Porcentagem de Filhos Melhores".format(dataset_name))
    plt.tight_layout()
    # plt.savefig('plots/{}/{}-best_child.png'.format(dataset_name, exp_name), dpi=300)
    plt.savefig('plots/final/{}/best_child.pdf'.format(dataset_name), dpi=300)
    plt.clf()


for dataset_name in exps_results:
    mkdirp("plots/final/{}/".format(dataset_name))

    plots = {}    
    plots["best_fit"] = 1
    plots["mean_fit"] = 2
    plots["worse_fit"] = 3
    plots["unique_ind_hist"] = 4

    best_fit_hist = []
    worse_fit_hist = []
    mean_fit_hist = []
    unique_ind_hist = []

    best_solutions = []

    for rep in exps_results[dataset_name]:
        data = exps_results[dataset_name][rep]

        best_fit_hist.append(data["best_fit_hist"])
        worse_fit_hist.append(data["worse_fit_hist"])
        mean_fit_hist.append(data["mean_fit_hist"])
        unique_ind_hist.append(data["unique_ind_hist"])
        best_solutions.append(data["last_population"][0])
    

    ## Convert to numpy
    best_fit_hist = np.array(best_fit_hist)
    worse_fit_hist = np.array(worse_fit_hist)
    mean_fit_hist = np.array(mean_fit_hist)
    unique_ind_hist = np.array(unique_ind_hist)
    best_solutions = np.array(best_solutions)


    ## Deal with early stops
    best_fit_hist[best_fit_hist == 0] = np.nan
    worse_fit_hist[worse_fit_hist == 0] = np.nan
    mean_fit_hist[mean_fit_hist == 0] = np.nan
    unique_ind_hist[unique_ind_hist == 0] = np.nan

    
    ## Filter Big values
    # best_fit_hist[best_fit_hist > 100 ] = 100
    # worse_fit_hist[worse_fit_hist > 100 ] = 100
    # mean_fit_hist[mean_fit_hist > 100 ] = 100
    # unique_ind_hist[unique_ind_hist > 100 ] = 100

    plt.figure(plots["best_fit"])
    for line in best_fit_hist:
        plt.plot(line, alpha=0.2, color="green")
    plt.plot(np.nanmean(best_fit_hist, axis=0), color="red")
    
    plt.figure(plots["mean_fit"])
    plt.plot(np.nanmean(mean_fit_hist, axis=0))

    plt.figure(plots["worse_fit"])
    plt.plot(np.nanmean(worse_fit_hist, axis=0))

    plt.figure(plots["unique_ind_hist"])
    plt.plot(np.nanmean(unique_ind_hist, axis=0))


    plt.figure(plots["best_fit"])
    plt.ylabel("Fitness")
    plt.xlabel("Geração")
    plt.title("{} - Melhor fitness por geração".format(dataset_name))
    plt.tight_layout()
    # plt.savefig('plots/{}/{}-best_fit.png'.format(dataset_name, exp_name), dpi=300)
    plt.savefig('plots/final/{}/best_fit.pdf'.format(dataset_name), dpi=300)
    plt.clf()

    plt.figure(plots["mean_fit"])
    plt.title("{} - Fitness média por geração".format(dataset_name))
    plt.tight_layout()
    # plt.savefig('plots/{}/{}-means_fit.png'.format(dataset_name, exp_name), dpi=300)
    plt.savefig('plots/final/{}/means_fit.pdf'.format(dataset_name), dpi=300)
    plt.clf()

    plt.figure(plots["worse_fit"])
    plt.title("{} - Pior fitness por geração".format(dataset_name))
    plt.tight_layout()
    # plt.savefig('plots/{}/{}-worse_fit.png'.format(dataset_name, exp_name), dpi=300)
    plt.savefig('plots/final/{}/worse_fit.pdf'.format(dataset_name), dpi=300)
    plt.clf()

    plt.figure(plots["unique_ind_hist"])
    plt.title("{} - Individuos únicos por geração".format(dataset_name))
    plt.ylabel("Quantidade de indivíduos únicos")
    plt.xlabel("Geração")
    plt.tight_layout()
    # plt.savefig('plots/{}/{}-unique_ind_hist.png'.format(dataset_name, exp_name), dpi=300)
    plt.savefig('plots/final/{}/unique_ind_hist.pdf'.format(dataset_name), dpi=300)
    plt.clf()



for dataset_name in exps_results:
    dataset = np.loadtxt("datasets/" + dataset_name + ".txt")
    x = dataset[:,0]
    y = dataset[:,1]
    best_ind = None
    best_fit = np.inf
    for rep in exps_results[dataset_name]:
        data = exps_results[dataset_name][rep]
        best_solutions = data["last_population"]

        fit = []
        for sol in best_solutions:
            fit.append(fitness(sol, dataset))

        b = np.argmin(fit)
        if fit[b] < best_fit:
            best_fit = fit[b]
            best_ind = best_solutions[b]


    if not "concrete" in dataset_name:
        y_pred = all_pred(best_ind, dataset)   

        plt.figure()
        plt.scatter(x=x, y=y, label="Dados de treino")
        plt.scatter(x=x, y=y_pred, label="Programação Genetica")
        plt.legend()
        plt.title("Dados de treino vs predições")
        plt.savefig('plots/final/{}/pred.pdf'.format(dataset_name), dpi=300)


    print(best_fit)
    print(pp(best_ind))
            