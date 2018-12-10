#!/usr/bin/env python
# -*- coding: utf-8 -*-

L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']

# print(L[:3])
# print(L[-1])

list1 = list(range(100))
# print(list1)
# print(list1[0:10])
# print(list1[-1])
# print(list1[-3:-2])


list2 = []
for x in range(1,11) :
    list2.append(x*x)
# print(list2)

print([x*x for x in range(1,11)])
# print([x*x for x in range(1,11) if x % 2 == 0])
# print([m*n for m in 'ABCD' for n in range(1,5)])
# print([m+n for m in 'ABCD' for n in 'XYZ'])

import os
# print(os.listdir('.'))
# print([d for d in os.listdir('.')])


# 列表生成器
# list3 = [x*x for x in range(10)]
# print(list3)

# g = (x*x for x in range(10))
# print(g)
# for i in g :
#     print(i)

from collections import Iterable
print(isinstance('adb', Iterable))






















