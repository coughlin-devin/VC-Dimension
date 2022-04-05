from SubsequenceDetection import SSD, popcnt_lookup32, count_runs, powerset_search, random_sample, combination_search
import numpy as np
import time

def main():
    #SSD_tests()
    #count_runs_tests()
    time_tests()

def SSD_tests():
    # False
    assert not SSD("0", "1")
    assert not SSD("1", "0")
    assert not SSD("1", "11")
    assert not SSD("101", "111")
    assert not SSD("101", "100")

    # True
    assert SSD("001", "00")
    assert SSD("101010", "111")
    assert SSD("1010101", "111")

def count_runs_tests():
    assert count_runs("1") == 1

def time_tests():
    # NOTE finished n=6,k=4 in 13 seconds: no shatterable set
    #powerset_shatter = shatter(5,4)
    # NOTE combination_search(19,12,8) executed in 325_964_517_900ns ~5m:26s
    combination_shatter = combination_search(8,6,5)

if __name__ == "__main__":
    main()
