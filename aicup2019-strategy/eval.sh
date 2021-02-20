cd aicup2019-linux
./aicup2019 --config config.json --save-results ../res.txt  --player-names  radac98 Basic &
# ./aicup2019 --batch-mode --config config.json --save-results ../res.txt &
cd ..
python3 main.py 127.0.0.1 31003 
cat res.txt
