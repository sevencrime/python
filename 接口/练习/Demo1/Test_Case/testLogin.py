#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import unittest
import xlrd
import json

class TestLogin(unittest.TestCase):

    excel_dir = 'F:\\python\\接口\\练习\\Demo1\\Test_Case\\data.xlsx'
    count = 0

    @classmethod
    def setUpClass(cls):
        #接口地址
        cls.login_url = 'http://127.0.0.1:5000/login'
        cls.info_url = 'http://127.0.0.1:5000/info'
        # cls.username = 'admin'
        # cls.password = '123456'
        cls.data = xlrd.open_workbook(cls.excel_dir)
        cls.table = cls.data.sheet_by_name(u'Sheet1')

    def test_login(self):
        table = self.table
        count = self.count

        for i in range(table.nrows):

            rows = table.row_values(i)
            
            data = {
                "username" : rows[0],
                "password" : int(rows[1])
            }

            try:
                # data 有两个参数,所有requests.post()返回一个字典
                response = requests.post(self.login_url,data=data).json()
            except TimeoutError:
                self.logger.error("Time out!")

            # print(type(response))
            for (d,x) in response.items(): #遍历response(字典)且输出
                print('传入参数',int(rows[1]),'response:',(d,x))

            assert response['code'] == 200
            assert response['msg'] == 'success'




if __name__ == '__main__' :
    unittest.main()



