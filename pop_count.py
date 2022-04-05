#%% Lookup table of number of set bits in binary representation of integers 0-255 (1 byte)
# https://graphics.stanford.edu/~seander/bithacks.html#CountBitsSetTable
BitsSetTable256 = [0]*256
for i in range(256):
    BitsSetTable256[i] = (i & 1) + BitsSetTable256[int(i / 2)]

# Return number of set bits in binary representation of 32 bit integers (4 bytes)
#   - uses lookup table to check each of the 4 bytes
def popcnt_lookup32(v):
    return BitsSetTable256[v & 0xff] + BitsSetTable256[(v >> 8) & 0xff] + BitsSetTable256[(v >> 16) & 0xff] + BitsSetTable256[v >> 24]
