import requests

# 登录禅道系统，登录api

class ZentaoAPI():

    def __init__(self, s):
        self.s = s

    # 函数1：登录禅道
    def login(self, account="admin", pwd="Tester123"):

        login_url = "http://192.168.3.3/zentaopms/www/index.php?m=user&f=login&referer=L3plbnRhb3Btcy93d3cvaW5kZXgucGhw"
        h = {
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        body = {
            "account": account,
            "password": pwd,
            "referer": "/zentaopms/www/index.php",
            "verifyRand": "967949977"
        }

        r = self.s.post(login_url, data=body, headers=h)
        # print(r.text)
        return r.text

    # 判断登录是否成功
    def isloginsuccess(self, res):
        exp = "parent.location="
        if exp in res:
            return True
        else:
            return False
