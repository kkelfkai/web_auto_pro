from common.HTMLReport import HTMLTestRunner

import unittest
import os


# 查找目录
curpath = os.path.dirname(__file__)
print(curpath)
startdir = os.path.join(curpath, "cases")

discover = unittest.defaultTestLoader.discover(startdir,
                                               pattern="test*.py",
                                               )
print(discover)

# 报告存放的路径
reportpath = os.path.join(curpath, "report", "result.html")
fp = open(reportpath, "wb")

# 生成报告

runner = HTMLTestRunner(stream=fp,
                        title="测试报告标题",
                        description="测试用例的描述")

runner.run(discover)
fp.close()
