#%% Decorator for timing function execution time
import time
def timer(func):
    def wrapper_timer(*args, **kwargs):
        start = time.perf_counter_ns()
        value = func(*args, **kwargs)
        stop = time.perf_counter_ns()
        elapsed_time = stop - start
        print(f'Function {func.__name__!r} executed in {elapsed_time:_}ns')
        return value
    return wrapper_timer

#%% Lookup table of number of set bits in binary representation of integers 0-255 (1 byte)
# https://graphics.stanford.edu/~seander/bithacks.html#CountBitsSetTable
BitsSetTable256 = [0]*256
for i in range(256):
    BitsSetTable256[i] = (i & 1) + BitsSetTable256[int(i / 2)]
# Return number of set bits in binary representation of 32 bit integers (4 bytes)
#   - uses lookup table to check each of the 4 bytes
def popcnt_lookup32(v):
    return BitsSetTable256[v & 0xff] + BitsSetTable256[(v >> 8) & 0xff] + BitsSetTable256[(v >> 16) & 0xff] + BitsSetTable256[v >> 24]

# IDEA: compare number of populated bits, if the 'subsequence' has more populated bits it's not a subsequence, can do same for zeroes: k-popcnt and n-popcnt
# IDEA: check number of runs to see if seq contains all subsequences, maybe add a row to the matrix marking if the subsequence column contains all subsequences (can be excluded from search) or not
# IDEA: if equal length, square matrix no shatterable set
# IDEA: combine above to reduce time
#%% Subsequence detection function O(n)
def SSD(seq,sub):
    n = len(seq)
    k = len(sub)

    # get population count of sequence and subsequence
    #seq_popcnt = popcnt_lookup32((int(seq, 2)))
    #sub_popcnt = popcnt_lookup32((int(sub, 2)))
    # if subsequence has more 1's or 0's than sequence it can't be a subsequence
    #if (sub_popcnt > seq_popcnt) or (k-sub_popcnt > n-seq_popcnt):
    #    return 0

    # WARNING on initial testing (6,3) and (5,4) slows down result
    #if count_runs(seq) > 2*k:
    #    return 1

    i = 0    # Index of string
    j = 0    # Index of sub

    while i < n and j < k:
        if seq[i] == sub[j]: # if sub character exists in seq
            j = j+1          # increment sub character
        i = i+1              # increment seq character

    if j == k:               # if sub index mathces length of sub, whole subsequence exists in seq
        return 1
    else:
        return 0

# returns a count of the number of runs in the sequence
def count_runs(seq):
    i = 1
    d = seq[0]
    r = 1
    while i < len(seq):
        if seq[i] != d:
            r = r+1
            d = seq[i]
        i = i+1
    return r

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

#%% takes an iterable and returns the powerset
from itertools import chain, combinations
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1)) # NOTE remove 1 to include empty set

# takes integer k and returns mapping of integers in range(2^k) to binary representation of k digits
def binary_mapping(n):
    mapping = map(lambda i: bin(i)[2:].zfill(n), range(2**n))
    return mapping

#IDEA use memoization somehow, know that if 0111 isn't a subset that 01111 also isn't?
"""
import math
@timer
def shatter(n,k):
    # TODO prefilter set
    # communication matrix
    cm = S(n,k)
    p = powerset(binary_mapping(n)) # OPTIMIZE?
    shatter_set = set()
    while len(subset:=next(p)) <= k: # NOTE while length of the subset is less than the upper bound
        if (len(shatter_set) == len(subset)): # NOTE if the shatter set is the same size as the subset, can skip checking for more equal length shatterable sets
            continue
        # for each subsequence
        comm_set = set()
        for i in range(2**k):
            #print(f"subsequence: \'{bin(i)[2:].zfill(k)}\'")
            comm_tuple = tuple()
            for sequence in subset:
                # add the value in communication matrix to tuple
                comm_tuple = comm_tuple + (cm[i][int(sequence,2)],)
            # add comm tuple to a set
            comm_set.add(comm_tuple)
        print(f"subset: {subset}, comm_set: {comm_set}")
        #print(f"length of comm_set: {len(comm_set)}, length of powerset: {2**k}, length of subset: {len(subset)}")
        # BUG this condition fails on n=5,k=4 because the largest shatterable set contains 3 sequences, not 4, and therefore the comm_matrix is size 2^3 not 2^4, so the condition won't be met
        if len(comm_set) == 2**len(subset): #len(subset)
            print(f"Shatterable set: {subset}")
            shatter_set = subset
    return shatter_set
"""

# helper to print out shatterable set in binary form
def print_shatter(iterable,n):
    shatter = []
    for i in iterable:
        shatter.append(bin(i)[2:].zfill(n))
    return shatter

# search the powerset in "increasing" order for shattered sets
@timer
def powerset_search(n,k):
    # TODO prefilter set
    # communication matrix
    cm = S(n,k)
    p = powerset(range(2**n)) # OPTIMIZE: replace with random sampling/prefilter
    # shatterable set
    shatter_set = set()
    # set of tuples of values of communication matrix
    comm_set = set()
    while len(subset:=next(p)) <= k: # NOTE while length of the subset is less than the upper bound
        #if (len(shatter_set) == len(subset)): # NOTE if the shatter set is the same size as the subset, can skip checking for more equal length shatterable sets
        #    continue
        # clear comm_set
        comm_set.clear()
        # for each subsequence
        for i in range(2**k):
            #print(f"subsequence: \'{bin(i)[2:].zfill(k)}\'")
            comm_tuple = tuple()
            for j in subset:
                # add the value in communication matrix to tuple
                comm_tuple = comm_tuple + (cm[i][j],)
            # add comm tuple to a set
            comm_set.add(comm_tuple)
        #print(f"subset: {subset}, comm_set: {comm_set}")
        #print(f"length of comm_set: {len(comm_set)}, length of powerset: {2**k}, length of subset: {len(subset)}")
        if len(comm_set) == 2**len(subset): #len(subset)
            shatter_set = subset
            print(f"Shatterable set: {print_shatter(shatter_set,n)}")
            for s in shatter_set:
                print(f"Column sums: {np.sum(cm,0)[s]}")
    return shatter_set

# create random samples of size s and check if it is a shattered set
from random import sample
@timer
def random_sample(n,k,s):
    cm = S(n,k)
    shatter_set = set()
    comm_set = set()
    while not shatter_set:
        rset = sample(range(2**n), s) # IDEA mess around with this range, maybe first/second half or middle half of the range is enough because of symmetry?
        comm_set.clear()
        for i in range(2**k):
            comm_tuple = tuple()
            for j in rset:
                comm_tuple = comm_tuple + (cm[i][j],)
            comm_set.add(comm_tuple)
        if len(comm_set) == 2**s:
            shatter_set = rset
            print(f"Shatterable set: {print_shatter(shatter_set,n)}")
            for s in shatter_set:
                print(f"Column sums: {np.sum(cm,0)[s]}")
    return shatter_set

# random sample on combinations of values with specific communication matrix column sums
def random_sample_filter(n,k,s):
    cm = S(n,k)
    shatter_set = set()
    comm_set = set()
    while not shatter_set:
        rset = sample(filter_cmatrix(cm, 2**(k-1)), s) # IDEA mess around with this range, maybe first/second half or middle half of the range is enough because of symmetry?
        comm_set.clear()
        for i in range(2**k):
            comm_tuple = tuple()
            for j in rset:
                comm_tuple = comm_tuple + (cm[i][j],)
            comm_set.add(comm_tuple)
        if len(comm_set) == 2**s:
            shatter_set = rset
            print(f"Shatterable set: {print_shatter(shatter_set,n)}")
            #for s in shatter_set:
            #    print(f"Column sums: {np.sum(cm,0)[s]}")
    return shatter_set

# find values with specified column sum in communication matrix
def filter_cmatrix(matrix, val):
    return [i for i,sum in enumerate(np.sum(matrix, axis=0)) if sum==val]

# search all combinations of size s from values with sepcified column sums in communication matrix
@timer
def combination_search(n,k,s):
    # communication matrix
    cm = S(n,k) # OPTIMIZE making this faster will speed up function a lot
    # shatterable set
    shatter_set = set()
    # set of tuples of values of communication matrix
    comm_set = set()
    # TODO expand to include range of column sums
    for comb in combinations(filter_cmatrix(cm, 2**(k-1)), s): # NOTE for each combinations of size s with column sums equal to v
        # clear comm_set
        comm_set.clear()
        # for each subsequence
        for i in range(2**k):
            #print(f"subsequence: \'{bin(i)[2:].zfill(k)}\'")
            comm_tuple = tuple()
            for j in comb:
                # add the value in communication matrix to tuple
                comm_tuple = comm_tuple + (cm[i][j],)
            # add comm tuple to a set
            comm_set.add(comm_tuple)
        #print(f"subset: {subset}, comm_set: {comm_set}")
        #print(f"length of comm_set: {len(comm_set)}, length of powerset: {2**k}, length of subset: {len(subset)}")
        if len(comm_set) == 2**s: #len(subset)
            shatter_set = comb
            print(f"Shatterable set: {shatter_set}, k={k}, n={n}, vc={s}")
            #for s in shatter_set:
            #    print(f"Column sums: {np.sum(cm,0)[s]}")
            return shatter_set

# TODO create a function to run combination_search for a while at different values to run overnight

# QUESTION How does raising n affect results? Will increasing n after not finding shattered set potentially create a shattered set without increasing k or s/vc?
# QUESTION Why did they choose n<=12? does it matter what n is when finding VC dimensions for k? Do they want the lowest n possible?
