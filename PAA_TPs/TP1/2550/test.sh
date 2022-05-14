clang++ -std=c++11 -O2 -lm main_kruskal.cpp -o kruskal
clang++ -std=c++11 -O2 -lm main_prim.cpp -o  prim
# ./a.out < in.txt > res.txt
# cat res.txt
# diff res.txt out.txt
# rm res.txt a.out