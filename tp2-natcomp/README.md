# tp2-natcomp

##Requirements
Install Python 3 and ´pip3 install --user -r requirements.txt´

## Usage

usage: main.py [-h] [-p POPSIZE] [-c CYCLES] [-n NCORES] [-d DATASET]
               [-lg LOG] [-id ID] [-q Q] [-prstnc PERSISTENCE]
               [-i INITIAL_TRAIL] [-a ALPHA] [-b BETA] [-pk PICKLE_ARGS] [-f]

Ant Colony Optimization

optional arguments:
  -h, --help            show this help message and exit
  -p POPSIZE, --popsize POPSIZE
                        Population size
  -c CYCLES, --cycles CYCLES
                        Max cycles
  -n NCORES, --ncores NCORES
                        Cores to run parallel
  -d DATASET, --dataset DATASET
                        Dataset file
  -lg LOG, --log LOG    Log folder
  -id ID, --id ID       Experiment id
  -q Q, --q Q           Trail Regulator
  -prstnc PERSISTENCE, --persistence PERSISTENCE
                        Trail persistence
  -i INITIAL_TRAIL, --initial-trail INITIAL_TRAIL
                        Initial trail
  -a ALPHA, --alpha ALPHA
                        Trail Importance
  -b BETA, --beta BETA  Visibility Importance
  -pk PICKLE_ARGS, --pickle-args PICKLE_ARGS
                        Pickle File with params [dataset, popsize, cycles,
                        log_dir, exp_id, p, initial_trail, q, cores, alpha,
                        beta]
  -f, --figs            Save Figures and generate GIF

  ## Experiments

  To generate the experiments run `python3 generate_exps.py` and `sh run_0.sh`

  Auxiliars scripts to plot the can be found in `plot_results/`
