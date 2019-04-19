# coding:utf-8

import unittest
import requests

# json解析，将response返回的结果解析成字典dict，可以按照对应的key取value


class Test_QiTa(unittest.TestCase):
    ''' caseSuit: Qita接口 '''

    @classmethod
    def setUpClass(cls):
        cls.url = "http://japi.juhe.cn/qqevaluate/qq"
        cls.s = requests.session()

    @classmethod
    def tearDownClass(cls):
        cls.s.close()

    def test_qq_1(self):
        ''' 测试QQ号码接口：key正确，qq号正确。期望结果：success '''
        par = {
            "key": "33d89bd3576cef4b93283d07f68c2ecc",
            "qq": "375785708"
        }

        r = self.s.get(self.url, params=par)
        res = r.json()["reason"]   # json转化成字典dict
        print("实际结果：%s" % res)
        self.assertTrue(res == "success")

    def test_qq_2(self):
        ''' 测试QQ号码接口：key错误，qq号正确。期望结果：KEY ERROR! '''
        par = {
            "key": "12345678",
            "qq": "375785708"
        }

        r = self.s.get(self.url, params=par)
        res = r.json()["reason"]   # json转化成字典dict
        print("实际结果：%s" % res)
        self.assertTrue(res == "KEY ERROR!")

    def test_qq_3(self):
        ''' 测试QQ号码接口：key正确，qq号为空。期望结果：错误的请求参数 '''
        par = {
            "key": "33d89bd3576cef4b93283d07f68c2ecc",
            "qq": ""
        }

        r = self.s.get(self.url, params=par)
        res = r.json()["reason"]   # json转化成字典dict
        print("实际结果：%s" % res)
        self.assertTrue(res == "错误的请求参数")


if __name__ == '__main__':
    unittest.main()
