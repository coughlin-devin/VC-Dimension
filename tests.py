from matrix_column_filter import shatter, random_column_search

def main():
    n = 9
    k = 6
    vc = 5
    l = 30 #2**(vc-1) # NOTE: 2^(S-1)<=column sum<=2^k-2^(S-1)
    u = 34 #2**k - 2**(vc-1)
    #shatter = random_column_search(n,k,vc,l,u)
    s = shatter(n,k,vc,l,u)
    print(s)

if __name__ == "__main__":
    main()
