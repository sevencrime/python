#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Students(object) :

    def __init__(self,name,age) :
        self.name = name
        self.age = age

    def get_grade(self) :
        if self.age >= 90:
            return 'A'
        elif self.age >=60 :
            return 'B'
        else :
            return 'C'



bart = Students("Amy", 10)
print(bart.name)
print(bart.age)
print(bart.name,bart.get_grade())
