#!/usr/bin/env python
# -*- coding: utf-8 -*-

# print(abs(-11))
# print(abs)
f = abs
# print(f(-10))

def add(x,y,f):
    return f(x) + f(y)

def f(x) :
    return x * x

r = map(f, [1,2,3,4,5])
print(list(map(f, [x for x in range(7)])))
print(list(map(str,[x for x in range(1,10)])))

from functools import reduce
def fn(x,y):
    return x * 10 + y

print(reduce(fn, [1,3,5,7,9]))
print(reduce(fn, [x for x in range(1,10) if x % 2 != 0]))








