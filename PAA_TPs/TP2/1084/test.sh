RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

clang++ -std=c++11 -O2 -lm main.cpp
for in in ./input/*
do
    out="${in/input/output}"
    my_out="./res.txt"

    ./a.out < $in > $my_out

    echo -n "Testing ${in}: "
    DIFF=$(diff $out $my_out)
    if [ "$DIFF" != "" ] 
    then
        echo -e "${RED}Fail${NC}"
    else
        echo -e "${GREEN}Passed${NC}"
    fi
done
# rm res.txt a.out