# TP1 - Busca

## Install Requirements:

### Python
- python3: `sudo apt-get install python3`
- pip: `sudo apt-get install python3-pip`

### Libs
- Required: `pip3 install -r requirements.txt --user `
- Optional: `pip3 install -r optional_requirements.txt --user`

## How to run:

### Using bash script:

`sh busca.sh -algoritmo {dfs,bfs,ids,a_star} -entrada {map_path.txt}`

### Using python script:

```
usage: src/main.py [-h] [-a {dfs,bfs,ids,a_star}] [-i INPUT] [-o OUTPUT] [-id ID] [-w W] [-v {-1,0,1,2,3,4}] [-t]

optional arguments:
  -h, --help            show this help message and exit
  -a {dfs,bfs,ids,a_star}, --algoritmo {dfs,bfs,ids,a_star}
                        Algoritmo de busca
  -i INPUT, --input INPUT
                        Mapa de entrada
  -o OUTPUT, --output OUTPUT
                        Diretorio de saida
  -id ID, --id ID       ID da execução
  -w W, --W W           ID da execução
  -v {-1,0,1,2,3,4}, --verbose {-1,0,1,2,3,4}
                        Print all info - Verbose 4 needs OpenCV and Matplotlib
  -t, --time            Time it

```

  