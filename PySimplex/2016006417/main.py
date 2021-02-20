import numpy as np
import sys
import os
from simplex2 import Simplex, DetectLC, printCert

if __name__ == "__main__":

    # Read Input
    mn_str = input()
    n,m = list(map(int, mn_str.split()))
    c_str = input()
    c = np.array(list(map(float, c_str.split())))
    Ab = np.zeros([n,m+1])
    for i in range(n):
        Ab[i] = np.array(list(map(float, input().strip().split())))

    A = Ab[:n, :m]
    b = Ab[:, -1]

    LC = DetectLC(A,b)
    LC = sorted(LC)[::-1]
    for i in LC:
        A = np.delete(A, i, 0)
        b = np.delete(b, i, 0)

    x = Simplex(A, b, c)
    mat = x.getTableaux()
    sol, cert, status, vo, _ = x.RunSimplex(mat)

    if not cert is None :
        cert = np.around(cert, 8)
    if not vo is None:
        vo = np.around(vo, 8)
    if not sol is None:
        sol = np.around(sol, 8)

    if status == 1:
        print("otima")
        print(vo)
        printCert(sol[:m])
        printCert(cert[:n])
    elif status == 2:
        print("ilimitada")
        printCert(sol[:m])
        printCert(cert[:m])
    elif status == 3:
        print("inviavel")
        printCert(cert[:n])