import numpy as np
import pandas as pd
import time
from random import sample
from itertools import combinations
from communication_matrix import S
from pop_count import popcnt_lookup32

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

# TODO should try to break apart massive dictionary copmprehension to make code readable
# OPTIMIZE look into using numpy functions in here, also set(map(tuple, iterable)) trick
# NOTE: returns a set of unique communication matrix column numbers whose column sums and population counts are within the given ranges
def filter_cmatrix(matrix,n,lsum,usum,lpc,upc):
    # NOTE not sure filtering duplicate columns is faster if have to do a dictionary copmprehension
    return set({tuple(matrix[:,i]) : i for i,sum in enumerate(np.sum(matrix,axis=0)) if sum <= usum and sum >= lsum and popcnt_lookup32(i) <= upc and popcnt_lookup32(i) >= lpc}.values())
    # IDEA filter out any unbalanced sequences with lots of 0s or lots of 1s, pop count less than floor(n/2) - 1 and greater than floor(n/2) + 1
    #return [i for i,sum in enumerate(np.sum(matrix, axis=0)) if sum <= upper and sum >= lower and popcnt_lookup32(i) <= (n/2 + 1) and popcnt_lookup32(i) >= (n/2 - 1)]

# IDEA look for combinations with close to 50/50 1 to 0 populated bits
# IDEA check to see where in communication matrix required columns are and create only those columns
# arguments: n = binary sequence length
#            k = binary subsequence length
#            vc = size of set attempting to shatter (vc dimension)
#            l = lower bound of column sum range: NOTE include sums >= l
#            u = upper bound of column sum range: NOTE include sums <= u
# behavior: search all combinations of size vc from subset of binary sequences length n with communication matrix column sums in range s-l <= sum <= s+u
# returns: shattered set if found, null otherwise
@timer
def shatter(n,k,vc,lsum,usum,lpc,upc):
    # list of dataframes of shattered sets
    #dfs = []
    # communication matrix
    cm = S(n,k)
    # TODO IDEA use combinations whose column sums are in a specific range of values: [comb for comb in combinations(filter_cmatrix(cm, l, u), 2) if sum([col_sums[num] for num in comb]) < 3] # < 3 is arbitrary condition
    # NOTE for each combination of size s with column sums in range 2**(k-1) - 0 <= sum <= 2**(k-1) + 0
    for comb in combinations(filter_cmatrix(cm,n,lsum,usum,lpc,upc), vc):
        # get an array of arrays by taking elements from the communication matrix with indeces of comb from each column
        array = np.take(cm,comb,axis=1)
        # remove duplicate arrays by converting array to a set of tuples
        array = set(map(tuple,array))
        if len(array) == 2**vc:
            # TODO add other interesting fields for analysis, maybe integer representation?
            dict = {"Sequence" : print_shatter(comb,n), "Column Sum" : [np.sum(cm,axis=0)[num] for num in comb], "Population Count" : [popcnt_lookup32(num) for num in comb]}
            shattered_set = pd.DataFrame(dict)
            print(shattered_set.to_string())
            #dfs.append(shattered_set)
            return shattered_set

@timer
def random_shatter(n,k,vc,lsum,usum,lpc,upc):
    # communication matrix
    cm = S(n,k)
    # set of integers representing the filterd column indexes of the communication matrix
    filtered = filter_cmatrix(cm,n,lsum,usum,lpc,upc)
    # while have not found a shattered set
    while 1:
        rset = sample(filtered, vc) # IDEA mess around with this range, maybe first/second half or middle half of the range is enough because of symmetry?
        # get an array of arrays by taking elements from the communication matrix with indeces of comb from each column
        array = np.take(cm,rset,axis=1)
        # remove duplicate arrays by converting array to a set of tuples
        array = set(map(tuple,array))
        if len(array) == 2**vc:
            dict = {"Sequence" : print_shatter(rset,n), "Column Sum" : [np.sum(cm,axis=0)[num] for num in rset], "Population Count" : [popcnt_lookup32(num) for num in rset]}
            shattered_set = pd.DataFrame(dict)
            print(shattered_set.to_string())
            return shattered_set

# IDEA start with small shattered set, use that set's integer values as start for search for larger shatterd set
# construct shattered set for (n+1,k+1) from set for (n,k)
# If shattered set exists in (n,k), it will be in the cm for larger n and k
