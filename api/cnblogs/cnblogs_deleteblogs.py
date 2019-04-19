import requests, re, time
from urllib.parse import unquote
from bs4 import BeautifulSoup


class CNBlogsDeletePostAPI():

    def __init__(self, s):
        self.s = s

    def getviewstate(self):
        url = "https://i.cnblogs.com/EditPosts.aspx?opt=1"
        h = {
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        self.s.headers.update(h)
        cks = requests.cookies.RequestsCookieJar()
        cks.set(".CNBlogsCookie",
                "4DC9D3D97C6474C0161A71DAFA939B64D14B2FBD2AD0D94D4B62871B5C85BF40E6287FD362E82AF201DB33D8D45D593BF0E72D6DFD24135AE8568CD2AAEC13CC85F11F0647D54D2ED7FC3847576ADE2FE8D77B74")
        cks.set(".Cnblogs.AspNetCore.Cookies",
                "CfDJ8JcopKY7yQlPr3eegllP76M4BIp26xz1wrbixmG-vQbeMRtr8AUpfOvPNkpFXevioz2nPTCEa9nA5pgA7vRiXqkXC-BJF01AOMQTOXYGNWTa-axY5T_9wWLyR3KYMSrf4Qr3GDJCFRjyu5-gLHk7is7mllDUkictRudrrAuN9TJhcDo40Ye7NFoGzQum1vYStyrmmPuLsKrtQzqndfViuMx0xH38ZGFV0gDsnKrk_KjdFj8GA-ymhENDk-rTj2HADwXydGQfW4vdywsow9pdOruJI9zSXjO1ogvZ61icSXjZ")
        self.s.cookies.update(cks)

        r = self.s.get(url, verify=False)
        # 获取动态参数__VIEWSTATE
        # BeautifulSoup获取html中的目标text
        soup = BeautifulSoup(r.text, "html.parser")
        tmp = soup.find(id="__VIEWSTATE")
        vs = tmp["value"]
        # print("__viewstate is: %s" % vs)
        return vs

    def getpostid(self, vs):
        addposturl = "https://i.cnblogs.com/EditPosts.aspx?opt=1"
        h = {
            "upgrade-insecure-requests": "1",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "referer": "https://i.cnblogs.com/"
        }
        self.s.headers.update(h)
        body = {
            "__VIEWSTATE": vs,
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
        r = self.s.post(addposturl, data=body, verify=False)

        url = unquote(r.url)  # from urllib.parse import unquote 解析url中的中文字符
        postid = re.findall("postid=(.+?)&", url)
        return postid[0]

    def deletepost(self, postid):
        delurl = "https://i.cnblogs.com/post/delete"

        h = {
            "x-requested-with": "XMLHttpRequest",
            "content-type": "application/json",
            "referer": "https://i.cnblogs.com/posts?postConfig=IsDraft"
        }
        self.s.headers.update(h)
        body = {
            "postId": postid
        }
        r = self.s.post(delurl, json=body, verify=False)
        tmp = r.json()
        # tmp = json.loads(r)
        return tmp["isSuccess"]  # true

    def isdeletesuccess(self, act):
        exp = True
        if exp == act:
            return True
        else:
            return False


if __name__ == '__main__':
    s = requests.session()
    cbd = CNBlogsDeletePostAPI(s)
    vs = cbd.getviewstate()
    pid = cbd.getpostid(vs)
    tmp = cbd.deletepost(pid)
    res = cbd.isdeletesuccess(tmp)
    print(res)


