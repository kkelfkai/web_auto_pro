from common.readexcel import ExcelUtil
from api.zentao.zentao_login import ZentaoAPI
import unittest
import requests
import ddt
import os


# testdatas = [
#     {"account": "admin", "psw": "Tester123", "exp": True},
#     {"account": "admin2", "psw": "3333", "exp": False},
#     {"account": "admin1", "psw": "1111", "exp": False},
#     {"account": "admin2", "psw": "2222", "exp": False},
# ]
# 此处不能使用相对路径,因为运行入口脚本的层级变化了，入口变成：runall_send_mail.py
# commonpath = os.path.dirname(__file__)
# print(commonpath)
# genpath = os.path.dirname(commonpath)
# datapath = os.path.join(genpath, "data")
# datafilepath = os.path.join(datapath, "test_data_zentao_login.xlsx")

# 找到绝对路径，先找到根目录，在join拼接
p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
filepath = os.path.join(p, "data", "test_data_zentao_login.xlsx")
sheetName = "Sheet1"
data = ExcelUtil(filepath, sheetName)
testdatas = data.dict_data()
print(testdatas)


@ddt.ddt
class TestZentaoLogin(unittest.TestCase):
    ''' 测试禅道登录api '''

    def setUp(self):
        self.s = requests.session()
        self.zt = ZentaoAPI(self.s)  # 实例化一个ZentaoAPI类对象

    def tearDown(self):
        self.s.close()

    @ddt.data(*testdatas)
    def test_login(self, data):
        # 使用{0}可以输出测试数据到测试报告里
        """ 测试数据：{0} """
        print("测试数据：%s" % str(data))
        # 1. 准备数据
        account = data["account"]
        pwd = data["pwd"]
        exp = bool(data["exp"])  # excel返回的是1和0， bool()转换为True 和 False

        # 2. 登录  （输入执行）
        res = self.zt.login(account, pwd)

        # 3. 获取实际结果
        act = self.zt.isloginsuccess(res)
        print("登录结果：%s" % act)

        # 4. 断言，实际结果与期望结果对比
        self.assertTrue(act == exp)
        # self.assertEqual(act, exp)  # 或者判断相等也可以
