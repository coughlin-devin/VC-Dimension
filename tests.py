from matrix_column_filter import column_search

def main():
    time_tests()

def time_tests():
    # NOTE column_search(19,12,8) executed in 325_964_517_900ns ~5m:26s on Devin's laptop
    shatter = column_search(6,3,3)

if __name__ == "__main__":
    main()
