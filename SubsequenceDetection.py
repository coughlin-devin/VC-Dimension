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
