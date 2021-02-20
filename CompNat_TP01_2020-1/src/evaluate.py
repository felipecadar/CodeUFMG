import numpy as np

#pythran export evaluate(int8[:], int, float64[:], int list)
def evaluate(arr, i, var, terminal):
    """Evaluate tree with variables.

    arr:    np.array        -> Genome 
    i:      int (default:0) -> Start index 
    var:    list            -> Variables 
    """
    l = arr.size

    if arr[i] in terminal:
        if arr[i] == 17: ## e
            return np.e
        if arr[i] == 18: ## pi
            return np.pi
        if arr[i] == 99:
            return 0
        elif arr[i] < 10: ## const
            # return float(arr[i])
            return float(arr[i])/float(10.0)
        else:
            print("Unkown node", arr[i])
            return 0
    
    elif arr[i] >= 100: ## variable
        return var[arr[i] - 100] 
    else:
        c1 = evaluate(arr, (i*2)+1, var, terminal)
        c2 = evaluate(arr, (i*2)+2, var, terminal)


        # print(c1, c2)

        if arr[i] == 10:
            return c1 + c2

        elif arr[i] == 11:
            return c1 - c2

        elif arr[i] == 12: # Protected Div
            if c2 == 0:
                # return 1
                return c1 / 0.000001
            return  c1 / c2

        elif arr[i] == 13:
            return c1 * c2

        elif arr[i] == 14:
            return np.power(c1, c2)

        elif arr[i] == 15:
            return np.power(c2, 2)

        elif arr[i] == 16:
            return np.exp(c2)
        
        elif arr[i] == 17:
            return np.log(c2)
