#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Students(object) :

    # 在变量名前加‘_’下划线，变成类的私有变量
    def __init__(self,name,age) :
        self._name = name
        self._age = age

    # 使用get方法供外部调用
    def get_name(self) :
        return self._name

    def get_age(self) :
        return self._age

    # 使用set方法供外部修改
    def set_age(self,age) : 
        self._age = age
        return age

    def get_grade(self) :
        if self._age >= 90:
            return 'A'
        elif self._age >=60 :
            return 'B'
        else :
            return 'C'



bart = Students("Amy", 10)
print(bart.get_age(),bart.get_name())

print(bart.get_grade())

print(bart.set_age(92))



