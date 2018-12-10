#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

def suite():
    loader = unittest.TestLoader()
    suite = loader.discover(r'F:\\Python_Demo\\python\\WEB编程\\接口测试\\unittest批量执行\\Test_Case')
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite',verbosity=2)

