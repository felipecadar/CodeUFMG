# CompNat_TP01_2020-1


## Instalation Debian/Ubuntu

### Dependencies

Install Python3 and Pip with
```
[sudo] apt-get install python3-dev python3-pip
```

Install lib dependencies with:
```
python3 -m pip install -r requirements.txt
```

### [Optional] For improved performance install `pythran` 

Pythran depends on a few Python modules and several C++ libraries. On a debian-like platform, run:

```
[sudo] apt-get install libatlas-base-dev
[sudo] apt-get install python3-ply python3-networkx python3-numpy
```

```
pip3 install pythran
```

**Compile Fitness Code**

Go to root directory and run: 

```
python3 src/compile_modules.py
```

## Running!

```
usage: main.py [-h] [--stop STOP] [-g GEN] [-s SIZE] [--seed SEED] [-k K]
               [-a ALPHA] [-f {ABS,MSE,RMSE}]
               [-p {ramped-hh,full,grow,descend-prob}] [-d DEPTH] [-e]
               [-i INPUT] [-o OUTPUT] [-c CORES] [--id ID]

optional arguments:
  -h, --help            show this help message and exit
  --stop STOP           Stop fitness value (default: 0.01)
  -g GEN, --gen GEN     Number of max generation (default: 1000)
  -s SIZE, --size SIZE  Population Size (default: 50)
  --seed SEED           Numpy random seed (default: -1)
  -k K, --K K           Tournament participation (default: 10)
  -a ALPHA, --alpha ALPHA
                        Crossover probability (default: 0.8)
  -f {ABS,MSE,RMSE}, --fitness {ABS,MSE,RMSE}
                        Fitness type (default: ABS)
  -p {ramped-hh,full,grow,descend-prob}, --population {ramped-hh,full,grow,descend-prob}
                        Initial population type (default: ramped-hh)
  -d DEPTH, --depth DEPTH
                        Tree max depth (default: 7)
  -e, --elit            Use Elitism (default: False)
  -i INPUT, --input INPUT
                        Input dataset file (default: datasets/01-SR_div.txt)
  -o OUTPUT, --output OUTPUT
                        Output results folder (default: results)
  -c CORES, --cores CORES
                        Parallel Cores. -1 means all cores (default: -1)
  --id ID               Experiment identifier. Time of execution as default
                        (default: )
```

Example:

Running with `grow` population, `RMSE` fitness, max depth of `4` and `30` individuals in population.

```
python3 src/main.py --size 30 --depth 4 --fitness RMSE --population grow
```

The output can be set with `--output` and the code will crate a folder there with its `--id` as name. The we save a pickle with a dict with all parameter, seed and results.


