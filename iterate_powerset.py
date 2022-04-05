from communication_matrix import S

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

# helper to print out shatterable set in binary form
def print_shatter(iterable,n):
    shatter = []
    for i in iterable:
        shatter.append(bin(i)[2:].zfill(n))
    return shatter

# search the powerset in "increasing" order for shattered sets
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
