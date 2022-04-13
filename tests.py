import pickle
import math
from matrix_column_filter import shatter

def main():
    n = 3
    k = 2
    vc = 2
    lsum = 2**(vc-1) # NOTE: 2^(S-1)<=column sum<=2^k-2^(S-1)
    usum = 2**k - 2**(vc-1)
    lpc = 1 #int(n/2) - 1
    upc = n-1 #int(n/2) + 1
    # diagonal array of nxk where arr[3][2] represents n=3,k=2
    #arr = [[[] for k in range(n)] for n in range(20)]

    # load array
    with open ('data', 'rb') as fp:
        arr = pickle.load(fp)

    #shatter = random_column_search(n,k,vc,l,u)
    dfs = shatter(n,k,vc,l,u)
    arr[n][k] = dfs
    # save array to file
    with open('data', 'wb') as fp:
        pickle.dump(arr, fp)

if __name__ == "__main__":
    main()
