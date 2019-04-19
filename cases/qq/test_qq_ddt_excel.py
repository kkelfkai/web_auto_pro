import unittest
import requests
import ddt
import os
from api.qqfortune.qqfortune import QQFortune
from common.readexcel import ExcelUtil

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
filepath = os.path.join(p, "data", "test_data_qqfortune.xlsx")
sheetName = "Sheet1"
data = ExcelUtil(filepath, sheetName)
test_datas = data.dict_data()
print(test_datas)

@ddt.ddt
class TestQQFortune(unittest.TestCase):

    def setUp(self):
        self.s = requests.session()
        self.qq = QQFortune(self.s)

    def tearDown(self):
        self.s.close()

    @ddt.data(*test_datas)
    def test_qqfortune(self, data):

        # 1. 准备数据
        key = data["key"]
        qq = data["qq"]
        exp = bool(data["exp"])

        # 2. 传入参数 & 执行
        act = self.qq.qqfortune(key, qq)
        self.assertTrue(exp == act)


if __name__ == '__main__':
    unittest.main()