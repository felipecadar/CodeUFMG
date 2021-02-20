#!/bin/bash
# python3 src/main.py --input $1 -v -1 --algoritmo $2

while test -n "$1"; do
    case "$1" in
      -c|-algoritmo)
          algoritmo=$2
          shift 2
          ;;  
      -d|-entrada)
          entrada=$2
          shift 2
          ;;
    esac
done 

# echo $algoritmo $entrada
python3 src/main.py --input $entrada -v -1 --algoritmo $algoritmo