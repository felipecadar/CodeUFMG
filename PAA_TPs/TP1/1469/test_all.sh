
clang++ -std=c++11 -O2 -lm 1469_static.cpp
# clang++ -std=c++11 -O2 -lm 1469_vector.cpp
for in in ./input/*
do
    out="${in/input/output}"
    my_out="./res.txt"

    ./a.out < $in > $my_out
    diff $out $my_out
done
rm res.txt a.out