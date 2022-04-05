# returns a count of the number of runs in the binary sequence (ex. "001001" => 4)
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
