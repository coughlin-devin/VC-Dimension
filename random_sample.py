from communication_matrix import S

# helper to print out shatterable set in binary form
def print_shatter(iterable,n):
    shatter = []
    for i in iterable:
        shatter.append(bin(i)[2:].zfill(n))
    return shatter

# create random samples of size s and check if it is a shattered set
from random import sample
def random_search(n,k,s):
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
