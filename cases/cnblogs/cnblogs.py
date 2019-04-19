# coding: utf-8

import unittest
import requests
import re
import time
from urllib.parse import unquote
from bs4 import BeautifulSoup


class TestAPICNBlogs(unittest.TestCase):
    '''  cnblogs新增/删除blog接口 '''

    def setUp(self):
        self.s = requests.session()

        # 获取登录cookies，获取动态参数viewstate[0]
        url1 = "https://i.cnblogs.com/EditPosts.aspx?opt=1"
        h = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        }
        self.s.headers.update(h)
        cks = requests.cookies.RequestsCookieJar()
        cks.set(".CNBlogsCookie",
                "C2EB773288F5362E39A83758CC7AE510E585308055905B30088E60117F469469ABE6033ABC3CB3C521CCC83EAED04E70A308E8C5D988F481165952C84D1A988281918C134C49BF72281175B2908B6902BDE62D4A")
        self.s.cookies.update(cks)
        r1 = self.s.get(url1, verify=False)
        res = r1.text

        #  BeautifulSoup获取html中的目标text
        soup = BeautifulSoup(res, "html.parser")
        tmp = soup.find(id="__VIEWSTATE")
        self.vs = tmp["value"]

        '''
        # 另一个方法：使用正则表达式找到__viewstate
        viewstate = re.findall('id="__VIEWSTATE" value="(.+?)"', res)
        self.vs = viewstate[0]  # urlencoded格式
        '''

        # 新增一个blog, 获取postid
        h1 = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded",
            "upgrade-insecure-requests": "1",
            "origin": "https://i.cnblogs.com",
            "referer": "https://i.cnblogs.com/"
        }
        self.s.headers.update(h1)  # 更新headers
        body = {

            "__VIEWSTATE": self.vs,
            "__VIEWSTATEGENERATOR": "FE27D343",
            "Editor$Edit$txbTitle": "test_%s" % str(time.time()),
            "Editor$Edit$EditorBody": "<p>test0455_%s</p>" % str(time.time()),
            "Editor$Edit$Advanced$ckbPublished": "on",
            "Editor$Edit$Advanced$chkDisplayHomePage": "on",
            "Editor$Edit$Advanced$chkComments": "on",
            "Editor$Edit$Advanced$chkMainSyndication": "on",
            "Editor$Edit$Advanced$txbEntryName": "",
            "Editor$Edit$Advanced$txbExcerpt": "",
            "Editor$Edit$Advanced$txbTag": "",
            "Editor$Edit$Advanced$tbEnryPassword": "",
            "Editor$Edit$lkbDraft": "存为草稿"

        }
        r2 = self.s.post(url1, data=body, verify=False)
        result1 = unquote(r2.url)  # unquote() 解析url中的中文字符
        print(result1)
        postid = re.findall("postid=(.+?)&", result1)
        self.pid = postid[0]
        actiontip = re.findall("actiontip=(.+?)$", result1)
        self.acid = actiontip[0]

    def tearDown(self):
        self.s.close()

    def test_cnblogs_addpost_1(self):
        '''新增blog，参数关联 actiontip '''
        self.assertIn("存为草稿成功", self.acid)

    def test_cnblogs_deletepost_2(self):
        '''删除blog，参数关联 postid '''
        url2 = "https://i.cnblogs.com/post/delete"
        h3 = {
            "x-requested-with": "XMLHttpRequest",
            "content-type": "application/json",
            "referer": "https://i.cnblogs.com/posts?postConfig=IsDraft"
        }
        self.s.headers.update(h3)
        body1 = {"postId": self.pid}
        r3 = self.s.post(url2, json=body1, verify=False)
        r4 = r3.json()
        # r4 = json.loads(r3)
        self.assertTrue(r4["isSuccess"], "删帖失败！")


