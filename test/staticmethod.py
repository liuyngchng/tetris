#!/usr/bin/python
# -*- coding: UTF-8 -*-


class C(object):
    @staticmethod
    def f():
        print('run oob')


if __name__ == '__main__':
    C.f()  # 静态方法无需实例化
    c_obj = C()
    c_obj.f()  # 也可以实例化后调用
