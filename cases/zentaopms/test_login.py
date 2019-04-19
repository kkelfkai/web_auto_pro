import requests
import unittest
import ddt
from api.zentao.zentao_login import ZentaoAPI


testdatas = [
    {"account": "admin", "psw": "Tester123", "exp": True},
    {"account": "admin2", "psw": "3333", "exp": False},
    {"account": "admin1", "psw": "1111", "exp": False},
    {"account": "admin2", "psw": "2222", "exp": False},
]

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
        ''' 测试登录接口'''

        print("测试数据：%s" % str(data))
        # 1. 准备数据
        account = data["account"]
        pwd = data["psw"]
        exp = bool(data["exp"])

        # 2. 登录  （输入执行）
        res = self.zt.login(account, pwd)

        # 3. 获取实际结果
        act = self.zt.isloginsuccess(res)
        print("登录结果：%s" % act)

        # 4. 断言，实际结果与期望结果对比
        self.assertTrue(act == exp)
        # self.assertEqual(act, exp)  # 或者判断相等也可以

