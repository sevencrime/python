#!/usr/bin/env python
# encoding: utf-8

import unittest

class test():
	status = "200"



class Mydemo(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		Mydemo.a = "88"
		test.status = "200"

	@unittest.skipIf(test.status == "200", "等于200")
	def test1(self):
		print(test.status, "11111111")
		test.status = "404"
		print(test.status, "333333333")

	@unittest.skipIf(test.status == "200", "等于404")
	def test2(self):
		print(test.status, "222222222")

if __name__ == '__main__':
    # unittest.main()
    li = set()
    print(len(li))