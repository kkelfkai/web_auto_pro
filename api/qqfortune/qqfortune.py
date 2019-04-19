import requests


class QQFortune():

    def __init__(self, s):
        self.s = s

    def qqfortune(self, key="33d89bd3576cef4b93283d07f68c2ecc", qq="37578570812"):
        qqurl = "http://japi.juhe.cn/qqevaluate/qq"
        par = {

            "key": key,
            "qq": qq

        }
        r = self.s.get(qqurl, params=par)
        # print(r.text)
        res = r.json()["reason"]  # 获取输出参数值，用于assert
        try:
            con = r.json()["result"]["data"]["analysis"]
        except:
            pass
        # print(con)

        if res == "success":
            print("结果：%s, 结果分析：%s" % (res, con))
            return True
        elif res == "KEY ERROR!":
            print("结果：%s" % res)
            return False
        elif res == "错误的请求参数":
            print("结果：%s" % res)
            return False
        else:
            print("结果：其他原因")
            return False


if __name__ == '__main__':
    s = requests.session()
    qq = QQFortune(s)
    qq.qqfortune()
