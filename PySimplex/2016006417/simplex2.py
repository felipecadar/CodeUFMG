"""
Simplex Implementation
Felipe Cadar Chamone - 2016006417
UFMG
"""

import numpy as np
np.set_printoptions(linewidth=500)
import logging as lg

# lg.basicConfig(format='[%(levelname)s]-%(message)s', level=lg.DEBUG)
lg.basicConfig(format='[%(levelname)s]-%(message)s', level=lg.INFO)

class Simplex():
    def __init__(self, A, b, c):
        self.n, self.m = A.shape
        self.eps = 0.0000000001
        self.dec = 10
        tableaux = self.MakeTableaux(A, b, c)
        tableaux = self.FixZeros(tableaux)
        self.tableaux = tableaux

    def RunSimplex(self, mat, identifier="Main"):
        running = True
        sol = None
        cert = None
        vo = 0
        status = -1
        simplex_iter = 0
        while running:
            lg.debug("[Simplex {}] Iter {}".format(identifier, simplex_iter))
            mat = self.FixZeros(mat)
            lg.debug(mat)

            # A = self.GetA(mat)
            B = self.GetB(mat)
            C = self.GetC(mat)
            
            if(self.hasNegative(B)):
                # Fix B and Aux!
                lg.debug("[RunSimplex] B has negative")
                mat = self.FixMatrixToSimplex(mat)
                mat, cert, succ = self.FindNewBases(mat)

                if succ == False:
                    lg.debug("[RunSimplex] PL is Inviable! {}".format(cert))
                    status = 3
                    running = False

            elif(self.hasNegative(C)):
                # Do it!
                lg.debug("[RunSimplex] C has negative")
                mat, succ, idx = self.SimplexStep(mat)
                if not succ:
                    # Ilimit :/
                    status =  2
                    cert = self.GetIlimitCert(mat, idx)
                    sol = self.GetSol(mat)
                    running = False
                    lg.debug("[RunSimplex] Ilimit {} {}".format(cert, sol))

            else:
                # End with optimal solution !
                status = 1
                cert = self.GetOptimalCert(mat)
                sol = self.GetSol(mat)
                vo = mat[0,-1]
                running = False
                lg.debug("[RunSimplex] Optimal {} {} {}".format(cert, sol, vo))

            simplex_iter += 1
        return sol, cert, status, vo, mat
 
    def FindNewBases(self, mat):
        cert = None
        succ = True

        bases = self.GetBases(mat)
        missing_bases = np.where(bases == -1)[0]
        
        if len(missing_bases) == 0:
            return mat, None, True

        aux, new_cols = self.CompleteMissingBases(mat.copy())
        aux[0,:] = 0
        for c in new_cols:
            aux[0,c] = 1

        for i in (missing_bases + 1):
            aux[0] -= aux[i]

        _, _, _, vo, aux = self.RunSimplex(aux, "Aux")
        # print(aux)
        simplex_bases = self.GetBases(aux)
        for b in simplex_bases:
            if b in new_cols:
                succ = False
            

        if succ:
            mat = self.Aux2Tabl(mat, aux)
            for i, b in enumerate(simplex_bases):
                mat = self.Pivot(mat, i+1, b)
        else:
            cert = self.GetInvCert(aux, missing_bases)

        return mat, cert, succ

    def Aux2Tabl(self, mat, aux):
        l,c = mat.shape
        mat[1:,:] = aux[1:, :c]
        mat[1:,-1] = aux[1:, -1]
        return mat

    def GetInvCert(self, mat, missing_bases):
        new_mat = mat[:, : mat.shape[1] - len(missing_bases) ]
        return self.GetOptimalCert(new_mat)

    def GetOptimalCert(self, mat):
        n = self.GetA(mat).shape[0]
        cert = mat[0, -n-1:-1]
        return cert

    def GetSol(self, mat):
        bases = self.GetBases(mat)
        sol = np.zeros(self.GetA(mat).shape[1])

        for i, b in enumerate(bases):
            sol[b] = self.GetB(mat)[i]

        return sol

    def GetIlimitCert(self, mat, j):
        A = self.GetA(mat)
        bases = self.GetBases(mat)
        cert = np.zeros(A.shape[1])
        cert[j] = 1
        for i, b in enumerate(bases):
            cert[b] = -A[i, j]
        
        return cert

    def SimplexStep(self, mat):
        l, c = mat.shape
        j = np.where(self.GetC(mat) < 0)[0][0]

        positive_idxs = np.where((mat[1:, j] > 0) * mat[1:, -1] > 0)[0]
        if len(positive_idxs) == 0:
            return mat, False, j

        positive_idxs += 1
        best_idx = positive_idxs[0]
        best_val = mat[best_idx,-1] / mat[best_idx, j]

        for i in positive_idxs[1:]:
            new_val = mat[i, -1] / mat[i, j]
            if new_val < best_val:
                best_idx = i
                best_val = new_val

        i = best_idx
        mat = self.Pivot(mat, i, j)
        mat = np.around(mat, self.dec)
        return mat, True, j


    
    def Pivot(self, mat, i, j):
        lines,cols = mat.shape
        for l in range(lines):
            if l != i:
                mat[l,:] = mat[l,:] - (mat[i,:] * (mat[l,j] / mat[i,j]))        
            else:
                mat[l,:] = mat[l,:] / mat[i,j]
        
        return mat
        

    def CompleteMissingBases(self, mat):
        l, c = mat.shape
        bases = self.GetBases(mat)
        missing_bases = np.where(bases == -1)[0]
        new_mat = np.zeros([l, c+len(missing_bases)])
        new_mat[:, 0:c-1] = mat[:, :-1]
        new_mat[:, -1] = mat[:, -1]

        new_cols = []
        for i, b in enumerate(missing_bases):
            col = c + i - 1
            new_cols.append(col)
            lin = b + 1
            new_mat[lin, col] = 1

        return new_mat, new_cols


    def GetBases(self, mat):
        l,c = mat.shape
        bases = np.ones([l-1], dtype=np.int) * -1
        for j in range(0, mat.shape[1]):
            col = mat[:,j]
            if bool(np.all(np.unique(col) == np.unique([0,1]))) and np.sum(col) == 1:
                idx = col[1:].nonzero()[0][0]
                if bases[idx] == -1:
                    bases[idx] = j

        return bases

    def getTableaux(self):
        return self.tableaux
    
    def FixZeros(self, mat):
        mat[np.abs(mat) < self.eps] = 0
        return mat

    def MakeTableaux(self, A, b, c):
        lines = self.n + 1
        cols = self.m + self.n + 1

        mat = np.zeros([lines, cols])

        mat[0, 0:self.m] = -1 * c
        mat[1:, 0:self.m] = A
        mat[1:, -1] = b

        mat[1:, self.m:self.m + self.n] = np.eye(self.n)
        return mat

    def FixMatrixToSimplex(self, mat):
        # Fix negatives in B
        for i in range(mat.shape[0]):
            if mat[i, -1] < 0:
                mat[i, :] *= -1
        return mat

    def GetA(self, mat):
        return mat[1:, :-1]

    def GetB(self, mat):
        return mat[1:, -1]

    def GetC(self, mat):
        return mat[0, 0:-1]

    def hasNegative(self, arr):
        if len(arr.shape) > 1:
            lg.error("[hasNegative]: Array needs to be 1 dim \n{}".format(arr))
            exit()

        return len(np.where(arr < 0)[0]) > 0


def DetectLC(A, b):
    """Remove lines there are linear combinations
        of other lines
    """
    mat = np.column_stack([A,b])
    mat[mat == 0] = 0.000000001
    LC = []
    for i in range(mat.shape[0]):
        for j in range(i+1, mat.shape[0]):
            if(j in LC):
                break
            c = mat[i, :] / mat[j, :]
            if len(np.unique(c)) == 1:
                LC.append(j)

    return LC

def printCert(cert):
    print(" ".join(list(map(str, cert))))