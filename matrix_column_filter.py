import numpy as np
import time
from communication_matrix import S
from itertools import combinations

#%% Decorator for timing function execution time
def timer(func):
    def wrapper_timer(*args, **kwargs):
        start = time.perf_counter_ns()
        value = func(*args, **kwargs)
        stop = time.perf_counter_ns()
        elapsed_time = stop - start
        print(f'Function {func.__name__!r} executed in {elapsed_time:_}ns')
        return value
    return wrapper_timer

# helper to print out shatterable set in binary form
def print_shatter(iterable,n):
    shatter = []
    for i in iterable:
        shatter.append(bin(i)[2:].zfill(n))
    return shatter

# find values with specified column sum in communication matrix
def filter_cmatrix(matrix, val):
    return [i for i,sum in enumerate(np.sum(matrix, axis=0)) if sum==val]

# search all combinations of size s from values with sepcified column sums in communication matrix
@timer
def column_search(n,k,s):
    # communication matrix
    cm = S(n,k) # OPTIMIZE make creating communication matrix faster
    # shatterable set
    shatter = set()
    # set of tuples of values from communication matrix
    comm_set = set()
    # TODO expand to include range of column sums
    for comb in combinations(filter_cmatrix(cm, 2**(k-1)), s): # NOTE for each combinations of size s with column sums equal to powers of 2**(k-1)
        # clear comm_set
        comm_set.clear()
        # for each subsequence
        for i in range(2**k):
            comm_tuple = tuple()
            for j in comb:
                # add the value from the communication matrix to a tuple
                comm_tuple = comm_tuple + (cm[i][j],)
            # add comm tuple to a set
            comm_set.add(comm_tuple)
        if len(comm_set) == 2**s:
            shatter = comb
            print(f"Shatterable set: {print_shatter(shatter,n) }, k={k}, n={n}, vc={s}")
            return shatter

# QUESTION How does raising n affect results? Will increasing n after not finding shattered set potentially create a shattered set without increasing k or s/vc?
# QUESTION Why did they choose n<=12? does it matter what n is when finding VC dimensions for k? Do they want the lowest n possible?
