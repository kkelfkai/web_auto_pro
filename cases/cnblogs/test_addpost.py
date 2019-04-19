import unittest
import requests
from api.cnblogs.cnblogs_addpost import CNBlogsAddPostAPI


class TestCNBlogsAddPost(unittest.TestCase):

    def setUp(self):
        self.s = requests.session()

    def tearDown(self):
        self.s.close()

    def test_addpost(self):
        cba = CNBlogsAddPostAPI(self.s)
        viewstate = cba.getviewstate()
        res = cba.addpost(viewstate)
        act = cba.isaddsuccess(res)
        print("添加blog结果：%s" % act)
        self.assertTrue(act, msg="添加blog失败！")


if __name__ == '__main__':
    unittest.main()
