import pickle
import math
from shatter_search import shatter, random_shatter

def main():
    n = 16
    k = 10
    vc = 7
    lsum = 2**(k-1) - int(math.log2(k)) #2**(vc-1) # NOTE: 2^(S-1)<=column sum<=2^k-2^(S-1)
    usum = 2**(k-1)  #2**k - 2**(vc-1)
    lpc = int(n/2) - 2
    upc = int(n/2) + 1

    # load diagonal array of lists of dataframes, each containing a shatterd set with column sum and population count information
    # arr[3][2] holds a list of dataframes for n=3, k=2. 
    with open ('data', 'rb') as fp:
        arr = pickle.load(fp)

    #dfs = shatter(n,k,vc,lsum,usum,lpc,upc)
    #arr[n][k] = dfs

    r = random_shatter(n,k,vc,lsum,usum,lpc,upc)
    arr[n][k].append(r)

    # save array to file
    with open('data', 'wb') as fp:
        pickle.dump(arr,fp)

if __name__ == "__main__":
    main()
