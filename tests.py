from matrix_column_filter import column_search, random_column_search

def main():
    n = 10
    k = 6
    vc = 5
    s = 2**(k-1)
    l = 2
    u = 0
    shatter = column_search(n,k,vc,s,l,u)
    print(shatter)

if __name__ == "__main__":
    main()
