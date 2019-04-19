
import requests


class CNBlogsLoginAPI():

    def __init__(self, s):
        self.s = s

    def login(self):
        loginurl = "https://i.cnblogs.com/EditPosts.aspx?opt=1"
        h = {
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        self.s.headers.update(h)
        cks = requests.cookies.RequestsCookieJar()
        cks.set(".CNBlogsCookie", "4DC9D3D97C6474C0161A71DAFA939B64D14B2FBD2AD0D94D4B62871B5C85BF40E6287FD362E82AF201DB33D8D45D593BF0E72D6DFD24135AE8568CD2AAEC13CC85F11F0647D54D2ED7FC3847576ADE2FE8D77B74")
        cks.set(".Cnblogs.AspNetCore.Cookies", "CfDJ8JcopKY7yQlPr3eegllP76M4BIp26xz1wrbixmG-vQbeMRtr8AUpfOvPNkpFXevioz2nPTCEa9nA5pgA7vRiXqkXC-BJF01AOMQTOXYGNWTa-axY5T_9wWLyR3KYMSrf4Qr3GDJCFRjyu5-gLHk7is7mllDUkictRudrrAuN9TJhcDo40Ye7NFoGzQum1vYStyrmmPuLsKrtQzqndfViuMx0xH38ZGFV0gDsnKrk_KjdFj8GA-ymhENDk-rTj2HADwXydGQfW4vdywsow9pdOruJI9zSXjO1ogvZ61icSXjZ")
        self.s.cookies.update(cks)

        r = self.s.get(loginurl, verify=False)
        return r.content.decode("utf-8")

    def isloginsuccess(self, res):
        exp = "博客后台管理 - 博客园"
        if exp in res:
            return True
        else:
            return False


if __name__ == '__main__':
    s = requests.session()  # 打开无界面的微型浏览器
    cb = CNBlogsLoginAPI(s)
    result = cb.login()
    act_result = cb.isloginsuccess(result)
    print("登录结果：%s" % act_result)
