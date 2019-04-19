import unittest
import requests
from api.cnblogs.cnblogs_deleteblogs import CNBlogsDeletePostAPI


class TestCNBlogsAddPost(unittest.TestCase):

    def setUp(self):
        self.s = requests.session()

    def tearDown(self):
        self.s.close()

    def test_deletepost(self):
        cbd = CNBlogsDeletePostAPI(self.s)
        vs = cbd.getviewstate()
        pid = cbd.getpostid(vs)
        tmp = cbd.deletepost(pid)
        res = cbd.isdeletesuccess(tmp)
        print("删除post结果：%s" % res)
        self.assertTrue(res, msg="添加blog失败！")


if __name__ == '__main__':
    unittest.main()
