import numpy as np

# OPTIMIZE Check quadrant and recurse on that quadrant, only have to check certain bits. recurse until k = 0 => return 1, or n = k
def S(n,k):
    if n == k:
        return np.identity(2**n)
    elif k == 0:
        return np.ones((1,2**n))
    else:
        b = S(n-1,k-1)
        U,L = np.split(S(n-1,k), 2, axis = 0)
        return np.block([[b,U],[L,b]])

# S(n,k) = |S(n-1,k-1)           U|
#          |L           S(n-1,k-1)|
