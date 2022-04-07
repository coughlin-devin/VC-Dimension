import numpy as np
import time
import math
from random import sample
from communication_matrix import S
from itertools import combinations
from tqdm import tqdm

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

# NOTE: returns a set of unique communication matrix column numbers whose column sums are within the given range
def filter_cmatrix(matrix, lower, upper):
    return set({tuple(matrix[:,i]) : i for i,sum in enumerate(np.sum(matrix, axis=0)) if sum <= upper and sum >= lower}.values())
    # [i for i,sum in enumerate(np.sum(matrix, axis=0)) if sum <= upper and sum >= lower]

#IDEA look for combinations with close to 50/50 1 to 0 populated bits
#IDEA remove duplicate values with identical columns
# arguments: n = binary sequence length
#            k = binary subsequence length
#            vc = size of set attempting to shatter (vc dimension)
#            l = lower bound of column sum range: NOTE include sums >= l
#            u = upper bound of column sum range: NOTE include sums <= u
# behavior: search all combinations of size vc from subset of binary sequences length n with communication matrix column sums in range s-l <= sum <= s+u
# returns: shattered set if found, null otherwise
@timer
def column_search(n,k,vc,l,u):
    # communication matrix
    cm = S(n,k) # OPTIMIZE make creating communication matrix faster
    # shatterable set
    shatter = set()
    # set of tuples of values from communication matrix
    comm_set = set()
    # IDEA use combinations whose column sums are in a specific range of values: [comb for comb in combinations(filter_cmatrix(cm, l, u), 2) if sum([col_sums[num] for num in comb]) < 3] # < 3 is arbitrary condition
    # NOTE for each combinations of size s with column sums in range 2**(k-1) - 0 <= sum <= 2**(k-1) + 0
    filtered = filter_cmatrix(cm, l, u)
    possible_shattered_sets = combinations(filtered, vc)
    bar = tqdm(possible_shattered_sets, total = math.comb(len(filtered), vc), colour="green")
    for comb in bar:
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
        if len(comm_set) == 2**vc:
            shatter = comb
            bar.close()
            print(f"Shattered set: {print_shatter(shatter,n) }, n={n}, k={k}, vc={vc}, l={l}, u={u}")
            return shatter

# random sample on combinations of values with specific communication matrix column sums
def random_column_search(n,k,s):
    cm = S(n,k)
    shatter = set()
    comm_set = set()
    # while have not found a shattered set
    while not shatter:
        rset = sample(filter_cmatrix(cm, 2**(k-1)), s) # IDEA mess around with this range, maybe first/second half or middle half of the range is enough because of symmetry?
        comm_set.clear()
        for i in range(2**k):
            comm_tuple = tuple()
            for j in rset:
                comm_tuple = comm_tuple + (cm[i][j],)
            comm_set.add(comm_tuple)
        if len(comm_set) == 2**s:
            shatter = rset
            print(f"Shatterable set: {print_shatter(shatter,n)}")
            return shatter
