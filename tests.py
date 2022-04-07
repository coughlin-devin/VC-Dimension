from matrix_column_filter import column_search, random_column_search

def main():
    n = 10
    k = 5
    vc = 5
    l = 2**(vc-1) # NOTE: 2^(S-1)<=column sum<=2^k-2^(S-1)
    u = 2**k - 2**(vc-1)
    shatter = column_search(n,k,vc,l,u)
    print(shatter)

if __name__ == "__main__":
    main()
