def knapSack(W, wt, val, n):
    K = [[0 for x in range(W + 1)] for x in range(n + 1)]
 
    # Build table K[][] in bottom up manner
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i-1] <= w:
                K[i][w] = max(val[i-1]+ K[i-1][w-wt[i-1]],  K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
    
    for line in K:
        print(line)
    return K[n][W], K
 
def getSol(K, val, wt, W):
    n, c = len(val), W
    sol = []
    while(n > 0 and c > 0):
        # print("Inspecting [{},{}]".format(n, c))
        now = K[n][c]
        opt1 = K[n-1][c-wt[n-1]] + val[n-1]
        opt2 = K[n-1][c]


        if opt1 > opt2: # included
            c = c - wt[n-1]
            sol.append(n-1)

        n = n-1

        # print("Next: [{},{}]".format(n, c))
    
    return sol



# Driver code
val = [92,57,49,68,60,43,67,84,87,72]
wt = [23,31,29,44,53,38,63,85,89,82]
W = 165
n = len(val)
soma, K = knapSack(W, wt, val, n)
sol = getSol(K, val, wt, W)
soma2 = sum([val[i] for i in sol])

correct = soma == soma2
print(correct)
