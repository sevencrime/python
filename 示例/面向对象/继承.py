#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Animal(object):
    """docstring for Animal"""
    def __init__(self):
        pass

    def run(self) :
        print("Animal is running")

class Dog(Animal) :
    def run(self) :
        print("Dog is running")

class Cat(Animal) :
    def run(self) :
        print("Cat is running")

dog = Dog()
dog.run()








