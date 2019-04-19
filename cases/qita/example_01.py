import requests
import urllib3
import re
import time
from urllib.parse import unquote

# 参数关联

urllib3.disable_warnings()


def test_login(s):
    # 获取登录cookies，返回动态参数
    url1 = "https://i.cnblogs.com/EditPosts.aspx?opt=1"
    h = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    }
    s.headers.update(h)  # 更细session中的headers
    # 获取cookies，更新session中的cookies
    cks = requests.cookies.RequestsCookieJar()
    cks.set(".CNBlogsCookie",
            "C2EB773288F5362E39A83758CC7AE510E585308055905B30088E60117F469469ABE6033ABC3CB3C521CCC83EAED04E70A308E8C5D988F481165952C84D1A988281918C134C49BF72281175B2908B6902BDE62D4A")
    s.cookies.update(cks)

    r1 = s.get(url1, headers=h, verify=False)
    # print(r1.text)
    res = r1.text
    viewstate = re.findall('id="__VIEWSTATE" value="(.+?)"', res)
    # print(viewstate[0])  # urlencoded格式

    # from urllib.parse import unquote
    # viewid = unquote(viewstate[0])
    # print(viewid)

    # 判断登录是否成功
    if "博客后台管理 - 博客园" in r1.text:
        print("登录成功")
    else:
        print("登录失败")

    return viewstate[0]


def test_addpost(s, viewstate):

    # 新增一个blog,参数关联 动态参数viewstate

    h1 = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "upgrade-insecure-requests": "1",
        "origin": "https://i.cnblogs.com",
        "referer": "https://i.cnblogs.com/"
    }
    s.headers.update(h1)  # 更新headers
    body = {

        "__VIEWSTATE": viewstate,
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
    url2 = "https://i.cnblogs.com/EditPosts.aspx?opt=1"
    r2 = s.post(url2, data=body, headers=h1, verify=False)
    result1 = unquote(r2.url)  # unquote() 解析url中的中文字符
    # print(result1)
    postid = re.findall("postid=(.+?)&", result1)
    if "存为草稿成功" in result1:
        print("新增成功")
        return postid[0]
    else:
        print("新增失败")


def test_deletepost(s, postid):

    # 删除添加的blog，参数关联 postid
    url3 = "https://i.cnblogs.com/post/delete"
    h3 = {
        "x-requested-with": "XMLHttpRequest",
        "content-type": "application/json",
        "referer": "https://i.cnblogs.com/posts?postConfig=IsDraft"
    }
    body1 = {"postId": postid}
    r3 = s.post(url3, json=body1, headers=h3, verify=False)
    r4 = r3.json()
    # r4 = json.loads(r3)
    if r4["isSuccess"] is True:
        print("删帖成功")
    else:
        print("删帖失败")


if __name__ == '__main__':
    s = requests.session()   # 创建当前会话对象
    viewstate = test_login(s)  # 获取登录cookies，返回动态参数viewstate
    postid = test_addpost(s, viewstate)  # 新增一条blog
    test_deletepost(s, postid)   # 删除新增的blog

