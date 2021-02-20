import subprocess
import shlex

try:
    import pythran
    print("Compiling evaluate code")
    M_NAME = "evaluate_module.cpython-36m-x86_64-linux-gnu.so"
    # cmd = "pythran -DUSE_XSIMD -fopenmp -march=native src/evaluate.py -o src/{}".format(M_NAME)
    cmd = "pythran src/evaluate.py -o src/{}".format(M_NAME)
    cmd = shlex.split(cmd)
    p = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    print("Done!")
except:
    print("Fail to find pythran module")
    print("Running without pythran optimization.")