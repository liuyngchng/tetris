#!/usr/bin/python
# -*- coding: UTF-8 -*-

a_tuple = (123, 'runoob', 'google', 'abc');
a_list = list(a_tuple)

if __name__ == '__main__':
    print(a_list)
    print(a_list[0], a_list[1])
    a_list[0] = 'test'
    a_list[1] = 456
    print(a_list)
    b_list = []
    # b_list[0] = 10          # error
    b_list.append(10)       # correct
    b_list.append([20, 30])
    b_list.append([40, 50])
    print('b_list=', b_list)
    print('b_list[0]=', b_list[0])
    print(b_list.index([40, 50]))
    a = [
        [11, 12, 13],
        [21, 22, 23],
        [31, 32, 33]
    ]
    print('len(a):', len(a))
    print('len(a[0]):', len(a[0]))
    for i in range(3):
        for j in range(3):
            print(a[i][j])
    zero = [
        [0, 0, 0],
        [0, 0, 0]
    ]
    for row in zero:
        if not sum(row):
            print("zero list")
