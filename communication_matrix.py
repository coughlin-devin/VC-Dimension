import numpy as np

def S(n,k):
    if n == k:
        return np.identity(2**n)
    elif k == 0:
        return np.ones((1,2**n))
    else:
        b = S(n-1,k-1)
        U,L = np.split(S(n-1,k), 2, axis = 0)
        return np.block([[b,U],[L,b]])

"""
@timer
def comm_matrix(n,k): # NOTE executes n=12, k=12 in 16 seconds
    # create zeroed array of size 2^n x 2^k/2
    arr = [[0 for i in range(2**n)] for j in range(int((2**k)/2))]

    # populate array with result of SSD # OPTIMIZE probably inneficient O(2^n * 2^k/2)
    for sub in range(int((2**k)/2)):
        for seq in range(2**n):
            arr[sub][seq] = SSD(bin(seq)[2:].zfill(n),bin(sub)[2:].zfill(k))

    # turn into numpy array
    half = np.array(arr)
    # flip array
    flip = np.flip(half)
    # concatenate half and flipped array into whole array
    m = np.concatenate((half, flip), axis=0)

    return m
"""
