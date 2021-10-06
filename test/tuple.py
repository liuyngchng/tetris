#!/usr/bin/python
from random import randrange
tup1 = ('physics', 'chemistry', 1997, 2000)
tup2 = (1, 2, 3, 4, 5, 6, 7)
tup3 = ('hello', 'who', 'are', 'you', '?', 6)

if __name__ == '__main__':
    print("tup1[0]: ", tup1[0])
    print("tup2[1:5]: ", tup2[1:5])
    tup_idx = randrange(0, len(tup3))
    print(tup_idx, tup3[tup_idx])
    print("tup3: ", tup3)
    tup4 = (
        (0, 1, 0, 0),
        (1, 1, 1, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0)
    )
    print("tup4: ", tup4)
    print("tup4[0]: ", tup4[0])
    print("tup4[0][1]: ", tup4[0][1])
    tup5 = ([0, 0], [-1, 0], [-2, 0], [1, 0])
    print("len(tup5):", len(tup5))
