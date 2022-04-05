from matrix_column_filter import column_search

def main():
    time_tests()

def time_tests():
    # NOTE finished n=6,k=4 in 13 seconds: no shatterable set
    #powerset_shatter = shatter(5,4)
    # NOTE combination_search(19,12,8) executed in 325_964_517_900ns ~5m:26s
    shatter = column_search(6,3,3)

if __name__ == "__main__":
    main()
